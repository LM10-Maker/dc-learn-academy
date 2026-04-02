// netlify/functions/stripe-webhook.js
// Handles Stripe checkout.session.completed → creates Supabase user + licence

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

const PRICE_MAP = {
  [process.env.STRIPE_PRICE_FOUNDING]: 'founding',
  [process.env.STRIPE_PRICE_STANDARD]: 'standard',
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
  const email = (session.customer_details?.email || session.customer_email || '').toLowerCase();

  if (!email) {
    console.error('No email in checkout session:', session.id);
    return { statusCode: 400, body: 'No customer email' };
  }

  // 3. Determine plan from line items or metadata
  //    Stripe checkout sessions include line_items only if expanded,
  //    so we also check session.metadata.price_id as a fallback.
  let plan = 'standard';
  try {
    const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
      expand: ['line_items'],
    });
    const priceId = fullSession.line_items?.data?.[0]?.price?.id
      || session.metadata?.price_id;
    if (priceId && PRICE_MAP[priceId]) {
      plan = PRICE_MAP[priceId];
    }
  } catch (err) {
    console.warn('Could not expand line_items, defaulting to standard:', err.message);
  }

  try {
    // 4. Create or find Supabase Auth user
    let userId;

    // Check if user already exists
    const { data: listData, error: listErr } = await supabase.auth.admin.listUsers({
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

    // 5. Guard against duplicate webhook delivery
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
        stripe_session_id: session.id,
        plan: plan,
        amount_paid: session.amount_total,
        currency: session.currency,
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

    console.log('Licence granted:', { userId, plan, sessionId: session.id });
    return { statusCode: 200, body: JSON.stringify({ received: true, userId, plan }) };

  } catch (err) {
    console.error('Webhook processing error:', err);
    return { statusCode: 500, body: `Processing error: ${err.message}` };
  }
};
