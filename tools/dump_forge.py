#!/usr/bin/env python3
"""Dump all Chinese content from Forge XML files."""
import os, re, sys

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')
COMMENT_RE = re.compile(r'<!--(.*?)-->', re.DOTALL)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

defs_root = os.path.join(REPO, 'Forge', '1.6', 'Defs')
for root, dirs, files in os.walk(defs_root):
    dirs.sort()
    for fname in sorted(files):
        if not fname.endswith('.xml'):
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, REPO).replace('\\', '/')
        with open(fpath, encoding='utf-8') as f:
            content = f.read()
        # Comments
        for m in COMMENT_RE.finditer(content):
            inner = m.group(1)
            if CHINESE_RE.search(inner):
                safe = inner.strip().replace('\n', '\\n')
                print(f'COMMENT|{rel}|{safe}')
        # Inline elements (non-comment lines with Chinese inside tags)
        for line in content.split('\n'):
            stripped = line.strip()
            if CHINESE_RE.search(stripped) and not stripped.startswith('<!--'):
                if '<' in stripped and '>' in stripped:
                    print(f'INLINE|{rel}|{stripped}')
