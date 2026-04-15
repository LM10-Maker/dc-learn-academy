#!/usr/bin/env node
// Extracts <script type="text/babel"> blocks from each HTML file and parses
// them with @babel/parser (jsx + flow plugins).  Reports PASS/FAIL per file.

const fs   = require('fs');
const path = require('path');
const babelParser = require('@babel/parser');

const netlifyDir = path.join(__dirname, 'netlify');
const files = [];
for (let i = 0; i <= 15; i++) {
  files.push(`dc-learn-${String(i).padStart(3, '0')}.html`);
}

let allPass = true;

for (const file of files) {
  const filePath = path.join(netlifyDir, file);
  let src;
  try {
    src = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    console.log(`FAIL  ${file}  [cannot read: ${e.message}]`);
    allPass = false;
    continue;
  }

  // Extract all <script type="text/babel"> ... </script> blocks
  const scriptRe = /<script[^>]+type=["']text\/babel["'][^>]*>([\s\S]*?)<\/script>/gi;
  const blocks = [];
  let m;
  while ((m = scriptRe.exec(src)) !== null) {
    blocks.push(m[1]);
  }

  if (blocks.length === 0) {
    console.log(`FAIL  ${file}  [no text/babel script block found]`);
    allPass = false;
    continue;
  }

  const combined = blocks.join('\n');

  try {
    babelParser.parse(combined, {
      sourceType: 'module',
      plugins: ['jsx', 'flow'],
      strictMode: false,
    });
    console.log(`PASS  ${file}`);
  } catch (e) {
    console.log(`FAIL  ${file}  [${e.message.split('\n')[0]}]`);
    allPass = false;
  }
}

process.exit(allPass ? 0 : 1);
