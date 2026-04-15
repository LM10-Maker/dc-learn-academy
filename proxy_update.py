#!/usr/bin/env python3
"""Replace direct Anthropic API calls with Supabase Edge Function proxy in all DC-TOOL v2.0 files."""
import glob, sys

EDGE_URL  = "https://iphonednnnqhxvhypvwn.supabase.co/functions/v1/tool-interpret"
ANON_KEY  = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
             ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwaG9uZWRubm5xaHh2aHlwdnduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQyMDU0MzMsImV4cCI6MjA4OTc4MTQzM30"
             ".VoexekmmKTbiLOBcROZl4YxUnx-A3EP8Rj7J72FBWAU")

# Exact strings found in every tool (verified by grep)
OLD_FETCH = "      const response = await fetch('https://api.anthropic.com/v1/messages', {"
NEW_FETCH = f"      const response = await fetch('{EDGE_URL}', {{"

OLD_HEADERS = "        headers: { 'Content-Type': 'application/json' },"
NEW_HEADERS = (f"        headers: {{ 'Content-Type': 'application/json',"
               f" 'Authorization': 'Bearer {ANON_KEY}' }},")

OLD_BODY = ("        body: JSON.stringify({\n"
            "          model: 'claude-sonnet-4-20250514',\n"
            "          max_tokens: 4000,\n"
            "          system: INTERPRETATION_PROMPT,\n"
            "          messages: [{ role: 'user', content: userPrompt }]\n"
            "        })")
NEW_BODY = ("        body: JSON.stringify({\n"
            "          system_prompt: INTERPRETATION_PROMPT,\n"
            "          user_message: userPrompt,\n"
            "          max_tokens: 8000\n"
            "        })")

files = sorted(glob.glob("tools/DC-TOOL-*_v2_0_0.html"))
print(f"Found {len(files)} v2.0 tool files\n")

errors = 0
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    if 'api.anthropic.com' not in original:
        print(f"  SKIP  {filepath} — no direct API call")
        continue

    content = original

    # 1. Replace URL
    if OLD_FETCH not in content:
        print(f"  ERROR {filepath} — fetch URL pattern not found (check indentation)")
        errors += 1
        continue
    content = content.replace(OLD_FETCH, NEW_FETCH, 1)

    # 2. Replace headers
    if OLD_HEADERS not in content:
        print(f"  ERROR {filepath} — headers pattern not found")
        errors += 1
        continue
    content = content.replace(OLD_HEADERS, NEW_HEADERS, 1)

    # 3. Replace body
    if OLD_BODY not in content:
        print(f"  ERROR {filepath} — body pattern not found")
        errors += 1
        continue
    content = content.replace(OLD_BODY, NEW_BODY, 1)

    # Sanity check: no more direct API calls
    if 'api.anthropic.com' in content:
        print(f"  ERROR {filepath} — still contains api.anthropic.com after replacement")
        errors += 1
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  DONE  {filepath}")

print(f"\n{'All done — no errors.' if errors == 0 else f'{errors} file(s) had errors — check above.'}")
sys.exit(errors)
