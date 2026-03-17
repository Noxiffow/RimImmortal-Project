#!/usr/bin/env python3
"""Find all large commented-out blocks containing Chinese in a mod's Defs."""
import re, sys, os, io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMMENT_RE = re.compile(r'<!--(.*?)-->', re.DOTALL)
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mod = sys.argv[1] if len(sys.argv) > 1 else 'Forge'
defs_root = os.path.join(REPO, mod, '1.6', 'Defs')

for root, dirs, files in os.walk(defs_root):
    dirs.sort()
    for fname in sorted(files):
        if not fname.endswith('.xml'):
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, REPO).replace('\\', '/')
        with open(fpath, encoding='utf-8') as fp:
            content = fp.read()
        for m in COMMENT_RE.finditer(content):
            inner = m.group(1)
            if CHINESE_RE.search(inner) and len(inner) > 200:
                print(f'{rel}: len={len(inner)}, preview={inner.strip()[:100]}')
