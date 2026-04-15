import shutil

SRC = "/home/user/dc-learn-academy/netlify/dc-learn-002.html"
DST = "/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html"

shutil.copy2(SRC, DST)
print(f"Copied {SRC} -> {DST}")

with open(DST, encoding='utf-8') as f:
    content = f.read()
print(f"File size: {len(content)} chars, {content.count(chr(10))+1} lines")
