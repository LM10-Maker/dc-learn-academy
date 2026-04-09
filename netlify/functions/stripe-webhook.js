// netlify/functions/stripe-webhook.js
// DC-LEARN Stage 5 — handles Stripe checkout.session.completed →
//   1. Verify signature
//   2. Create or find Supabase auth user for the customer email
//   3. Insert row into `licences` with tier mapped from Stripe price ID
//   4. Send magic link so the learner can sign in immediately
//
// Four tiers (live prices):
//   €995       one-off     → founding
//   €1,995     one-off     → professional
//   €9,500/yr  subscription → corporate
//   €18,000+   one-off/sub  → enterprise

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Stripe price-id → tier mapping. Price IDs come from the Stripe dashboard
// and are injected via Netlify environment variables.
const PRICE_MAP = {
  [process.env.STRIPE_PRICE_FOUNDING]:     'founding',
  [process.env.STRIPE_PRICE_PROFESSIONAL]: 'professional',
  [process.env.STRIPE_PRICE_CORPORATE]:    'corporate',
  [process.env.STRIPE_PRICE_ENTERPRISE]:   'enterprise',
};

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  // 1. Verify Stripe signature
  const sig = event.headers['stripe-signature'];
  let stripeEvent;
  try {
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error('Signature verification failed:', err.message);
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }

  // 2. Only handle checkout.session.completed
  if (stripeEvent.type !== 'checkout.session.completed') {
    return { statusCode: 200, body: 'Ignored' };
  }

  const session = stripeEvent.data.object;
  const email = (session.customer_details?.email || session.customer_email || '')
    .toLowerCase();

  if (!email) {
    console.error('No email in checkout session:', session.id);
    return { statusCode: 400, body: 'No customer email' };
  }

  // 3. Determine tier + amount + expiry from line items / subscription
  let tier = null;
  let amountCents = session.amount_total || null;
  let currency = session.currency || 'eur';
  let expiresAt = null;
  let paymentIntentId = session.payment_intent || null;

  try {
    const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
      expand: ['line_items', 'subscription'],
    });

    const priceId = fullSession.line_items?.data?.[0]?.price?.id
      || session.metadata?.price_id;

    if (priceId && PRICE_MAP[priceId]) {
      tier = PRICE_MAP[priceId];
    }

    // For subscription checkouts (corporate tier), grab period-end as expiry.
    if (fullSession.mode === 'subscription' && fullSession.subscription) {
      const sub = typeof fullSession.subscription === 'string'
        ? await stripe.subscriptions.retrieve(fullSession.subscription)
        : fullSession.subscription;
      if (sub && sub.current_period_end) {
        expiresAt = new Date(sub.current_period_end * 1000).toISOString();
      }
    }
  } catch (err) {
    console.warn('Could not expand checkout session:', err.message);
  }

  if (!tier) {
    // Unknown price id → infer from amount as a last-resort (avoids silent drops).
    if (amountCents >= 1800000)      tier = 'enterprise';
    else if (amountCents >= 950000)  tier = 'corporate';
    else if (amountCents >= 199500)  tier = 'professional';
    else if (amountCents >= 99500)   tier = 'founding';
    else {
      console.error('Could not map price to tier. Session:', session.id, 'amount:', amountCents);
      return { statusCode: 400, body: 'Unknown price / tier' };
    }
    console.warn('Tier inferred from amount:', tier);
  }

  try {
    // 4. Create or find Supabase Auth user
    let userId;
    const { data: listData } = await supabase.auth.admin.listUsers({
      filter: `email.eq.${email}`,
    });
    // listUsers filter may not work on all Supabase versions — fallback to scan
    const existingUser = listData?.users?.find(u => u.email === email);

    if (existingUser) {
      userId = existingUser.id;
    } else {
      const { data: newUser, error: createErr } = await supabase.auth.admin.createUser({
        email: email,
        email_confirm: true,
      });
      if (createErr) throw createErr;
      userId = newUser.user.id;
    }

    // 5. Idempotency guard — skip if this Stripe session already has a licence
    const { data: existingLicence } = await supabase
      .from('licences')
      .select('id')
      .eq('stripe_session_id', session.id)
      .maybeSingle();

    if (existingLicence) {
      console.log('Duplicate webhook — licence already exists for session:', session.id);
      return { statusCode: 200, body: JSON.stringify({ received: true, duplicate: true }) };
    }

    // 6. Insert licence record
    const { error: licErr } = await supabase
      .from('licences')
      .insert({
        user_id: userId,
        stripe_customer_id: session.customer,
        stripe_payment_intent_id: paymentIntentId,
        stripe_session_id: session.id,
        tier: tier,
        amount_cents: amountCents,
        currency: currency,
        status: 'active',
        expires_at: expiresAt,
      });

    if (licErr) throw licErr;

    // 7. Send magic link so the learner can log in immediately
    try {
      await supabase.auth.admin.generateLink({
        type: 'magiclink',
        email: email,
        options: {
          redirectTo: `${process.env.SITE_URL}/login.html?welcome=true`,
        },
      });
    } catch (magicErr) {
      // Non-fatal — learner can request a link from the login page
      console.warn('Magic link generation failed:', magicErr.message);
    }

    console.log('Licence granted:', { userId, tier, sessionId: session.id, expiresAt });
    return {
      statusCode: 200,
      body: JSON.stringify({ received: true, userId, tier }),
    };

  } catch (err) {
    console.error('Webhook processing error:', err);
    return { statusCode: 500, body: `Processing error: ${err.message}` };
  }
};
