#!/usr/bin/env python3
"""
fix_bizarre_keys.py  —  Corrects wrong Unicode escapes in translate_bizarre_comments.py.
All replacements work on the RAW TEXT of the source file (literal \\uXXXX sequences).
Run once: python tools/fix_bizarre_keys.py
"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(REPO, "tools", "translate_bizarre_comments.py")

with open(TARGET, encoding="utf-8") as f:
    src = f.read()
original = src

# ─────────────────────────────────────────────────────────────────────────────
# All find/replace strings use ONLY raw strings (r'...') so that \uXXXX and \n
# are treated as literal character sequences matching the source file text.
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS = [
    # ── AoJing / AoJing_Defs: 趾 \u8d3e → \u8dbe ─────────────────────────
    (r'\u811a\u8d3e', r'\u811a\u8dbe'),

    # ── BingJia: 沾 \u6cbf → \u6cbe ──────────────────────────────────────
    (r'\u6cbf\u67d3\u715e', r'\u6cbe\u67d3\u715e'),

    # ── ZhengDe: zen sound desc — literal \n → \\n, fix chars ─────────────
    # Source: \u3002\n\u89e3\u9664\u8fe5\u8292  (backslash-n + wrong chars)
    # Target: \u3002\\n\u89e6\u9664\u8ff7\u832b (escaped newline + right chars)
    (r'\u3002\n\u89e3\u9664\u8fe5\u8292', r'\u3002\\n\u89e6\u9664\u8ff7\u832b'),

    # ── ZhengDe: "明心" — escaped quotes → curly quotes ──────────────────
    # Source has: \"\\u660e\\u5fc3\"  (backslash-quote)
    (r'\"\\u660e\\u5fc3\"', r'\\u201c\\u660e\\u5fc3\\u201d'),

    # ── ZhengDe: almsgiving desc — literal \n → \\n ───────────────────────
    (r'\u9e70\n \u8865\u5145', r'\u9e70\\n \u8865\u5145'),

    # ── ZhengDe: "舍身" — escaped quotes → curly quotes ──────────────────
    (r'\"\\u820d\\u8eab\"', r'\\u201c\\u820d\\u8eab\\u201d'),

    # ── ZhengDe: meditation desc — literal \n\n → \\n\\n ──────────────────
    (r'\u4e0a\u5347\n\n \u5176\u4ed6', r'\u4e0a\u5347\\n\\n \u5176\u4ed6'),

    # ── ZhengDe_Enlightenment: angry gaze desc — fix chars + quotes ────────
    # Source: \"\\u6012\\u76ee\\u91d1\\u5c71\\u762b\\u76ee\\u89c6...\\u523b...\"
    # Target: \\u201c...\\u521a...\\u778b...\\u5239...\\u201d
    (
        r'\"\\u6012\\u76ee\\u91d1\\u5c71\\u762b\\u76ee\\u89c6\\uff0c\\u6076\\u523b\\u5996\\u9b54\\u7686\\u80c6\\u88c2\\u3002\"',
        r'\\u201c\\u6012\\u76ee\\u91d1\\u521a\\u778b\\u76ee\\u89c6\\uff0c\\u6076\\u5239\\u5996\\u9b54\\u7686\\u80c6\\u88c2\\u3002\\u201d',
    ),

    # ── ZhengDe_Enlightenment: lion's roar — 慌(6174) → 慑(6151) ──────────
    (r'\u9707\u6174\u5bf9\u65b9', r'\u9707\u6151\u5bf9\u65b9'),

    # ── ZhengDe_Enlightenment: dizziness key — 晕(6657) → 晕(6655) ─────────
    (r'\u5934\u6657\u8033\u9e23', r'\u5934\u6655\u8033\u9e23'),

    # ── ZhengDe_Enlightenment / BodyParts: 梅(6885)→梵(68b5) ──────────────
    (r'\u6885\u754c', r'\u68b5\u754c'),
    (r'\u6885\u9e23\u80ba', r'\u68b5\u9e23\u80ba'),

    # ── ZhengDe_Enlightenment: shield pack — 搑(64d1) → 摑(6491) ───────────
    (r'\u64d1\u8d77', r'\u6491\u8d77'),

    # ── ZhengDe_Enlightenment: 慈悟(609f) → 慈悲(60b2) ─────────────────────
    (r'\u6148\u609f\u638c', r'\u6148\u60b2\u638c'),

    # ── ZhengDe_Enlightenment: 巧(52c1)→(52b2) ──────────────────────────
    (r'\u5de7\u52c1\u653b\u51fb', r'\u5de7\u52b2\u653b\u51fb'),

    # ── ZhengDe_Enlightenment: 撥(6714)→撼(64bc) ────────────────────────
    (r'\u6714\u5c71\u62f3', r'\u64bc\u5c71\u62f3'),

    # ── ZhengDe_Enlightenment: 嶳(5c73)→岳(5cb3) ───────────────────────
    (r'\u5c71\u5c73\u7684\u4e00\u62f3', r'\u5c71\u5cb3\u7684\u4e00\u62f3'),

    # ── ZhengDe_Sacrifice / ZhengDe hediff / SoundDefs: 皯(796f)→嘶(5636) ─
    (r'\u6050\u6016\u796f\u543c', r'\u6050\u6016\u5636\u543c'),
    (r'\\u796f\\u543c": "Scream"', r'\\u5636\\u543c": "Scream"'),

    # ── ZhengDe_Sacrifice / ZhengDe hediff: 厄(5384)→噩(5669) ─────────────
    (r'\u5384\u68a6\u51dd\u89c6', r'\u5669\u68a6\u51dd\u89c6'),

    # ── ZhengDe_Tathagata: 掛(639b)→掷(63b7) ────────────────────────────
    (r'\u98de\u639b ', r'\u98de\u63b7 '),

    # ── ZuoWang: 讹(8bd3)→讳(8bf3) ──────────────────────────────────────
    (r'\u6df7\u73e0\u8bd3\u53d6', r'\u6df7\u73e0\u8bf3\u53d6'),

    # ── ZuoWang: 误(8bef)→诰(8bf0) ──────────────────────────────────────
    (r'\u7f54\u5929\u5b9d\u8bef', r'\u7f54\u5929\u5b9d\u8bf0'),

    # ── ZuoWang_Defs: 蛎(86ce)→蚩(86a9) ────────────────────────────────
    (r'\u86ce\u5c24\u6012\u708e', r'\u86a9\u5c24\u6012\u708e'),

    # ── ZuoWang_Defs: 钆(9486)→钵(94b5) ────────────────────────────────
    (r'\u91d1\u9486\u3010', r'\u91d1\u94b5\u3010'),

    # ── ZuoWang_Defs: 抩(62a9)→抚(629a) ────────────────────────────────
    (r'\u5fc3\u7075\u62a9\u6170', r'\u5fc3\u7075\u629a\u6170'),

    # ── HediffDefs/ZhengDe: 铂(9502)→锢(9522) ───────────────────────────
    (r'\u7981\u9502', r'\u7981\u9522'),

    # ── HediffDefs/ZhengDe: 祸(7978)→祟(795f) ───────────────────────────
    (r'\u90aa\u7978\u96be', r'\u90aa\u795f\u96be'),

    # ── HediffDefs/ZhengDe: 溃溃(6e83 6e83)→崩溃(5d29 6e83) ───────────
    (r'\u9020\u6210\u6e83\u6e83', r'\u9020\u6210\u5d29\u6e83'),

    # ── HediffDefs/ZhengDe: 呀(5440)→呕(5455) ───────────────────────────
    (r'\u4f1a\u5440\u5410', r'\u4f1a\u5455\u5410'),

    # ── BodyParts/ZhengDe_Enlightenment: 诵(9b21)→颂(9882) ─────────────
    (r'\u5ff5\u9b21\u58f0', r'\u5ff5\u9882\u58f0'),

    # ── BodyParts/ZhengDe_Enlightenment: 慌(6174)→慑(6151) in 震 ─────────
    (r'\u9707\u6174\u4f17\u751f', r'\u9707\u6151\u4f17\u751f'),

    # ── BodyParts/ZhengDe_Enlightenment: 蛌(868c)→蟬(866c) ─────────────
    (r'\u808c\u8089\u868c\u7ed3', r'\u808c\u8089\u866c\u7ed3'),

    # ── BodyParts/ZhengDe_Enlightenment: 挔(6514)→撼(64bc) ─────────────
    (r'\u6514\u5c71\u62f3', r'\u64bc\u5c71\u62f3'),

    # ── BodyParts/ZhengDe_Enlightenment: lotus leg \n\n ─────────────────
    (r'\u3002\n\n \u9644\u52a0\u80fd\u529b\uff1a\u5706\u5149\u817f',
     r'\u3002\\n\\n \u9644\u52a0\u80fd\u529b\uff1a\u5706\u5149\u817f'),

    # ── BodyParts/ZhengDe_Enlightenment: 花开...brahma — \n\n + 梅→梵 ──
    (r'\u83b2\u3002\n\n \u9644\u52a0\u80fd\u529b\uff1a\u6885\u754c',
     r'\u83b2\u3002\\n\\n \u9644\u52a0\u80fd\u529b\uff1a\u68b5\u754c'),

    # ── BodyParts/ZhengDe_Restraint: "菩提本无树" escaped→curly ────────
    (r'\"\\u83e9\\u63d0\\u672c\\u65e0\\u6811\\uff0c\\u660e\\u955c\\u4ea6\\u975e\\u53f0\"',
     r'\\u201c\\u83e9\\u63d0\\u672c\\u65e0\\u6811\\uff0c\\u660e\\u955c\\u4ea6\\u975e\\u53f0\\u201d'),

    # ── BodyParts/ZhengDe_Restraint: 齋(9f4b)→斋(658b) ──────────────────
    (r'\u9f4b\u85cf\u80c3', r'\u658b\u85cf\u80c3'),

    # ── BodyParts/ZhengDe_Restraint: 抗拔(6297 62d4)→抵抗(62b5 6297) ───
    (r'\u6bd2\u7d20\u6297\u62d4', r'\u6bd2\u7d20\u62b5\u6297'),

    # ── BodyParts/ZhengDe_Restraint: "欲速" escaped→curly ──────────────
    (r'\"\\u6b32\\u901f\\u5219\\u4e0d\\u8fbe\\u3002\"',
     r'\\u201c\\u6b32\\u901f\\u5219\\u4e0d\\u8fbe\\u3002\\u201d'),

    # ── BodyParts/ZhengDe_Restraint: 贪(8daa)→贪(8d2a) ──────────────────
    (r'\u82e5\u8daa\u56fe', r'\u82e5\u8d2a\u56fe'),

    # ── BodyParts/ZhengDe_Restraint: \u60089 → \u6089 (悉) ─────────────
    (r'\u8574\u60089\u4ece', r'\u8574\u6089\u4ece'),

    # ── BodyParts/ZhengDe_Restraint: 耣(8783)→耘(8018) ─────────────────
    (r'\u8015\u8783\u3002', r'\u8015\u8018\u3002'),

    # ── BodyParts/ZhengDe_Restraint: 逝(901d)→速(901f) ─────────────────
    (r'\u6316\u6398\u901d\u5ea6', r'\u6316\u6398\u901f\u5ea6'),

    # ── BodyParts/ZhengDe_Sacrifice: 腥(8165)→猩(7329) ──────────────────
    (r'\u8165\u7ea2\u773c', r'\u7329\u7ea2\u773c'),
    (r'\u8165\u7ea2\u7684', r'\u7329\u7ea2\u7684'),

    # ── BodyParts/ZhengDe_Sacrifice: 证(8bc1)→诡(8be1) ──────────────────
    (r'\u8bc1\u5f02\u7684\u7eb9\u8def', r'\u8be1\u5f02\u7684\u7eb9\u8def'),

    # ── BodyParts/ZhengDe_Sacrifice: 肂(8082)→肝(809d) ──────────────────
    (r'\u589e\u751f\u8082', r'\u589e\u751f\u809d'),

    # ── BodyParts/ZhengDe_Sacrifice: tentacle \n\n + 傅(5085)→傩(50a9) ──
    (r'\u52a8\u7740\uff0c\n\n\u5728\'\u5927\u5085\'',
     r'\u52a8\u7740\uff0c\\n\\n\u5728\'\u5927\u50a9\''),

    # ── BodyParts/ZhengDe_Sacrifice: 腾(817e)→腐(8150) ──────────────────
    (r'\u817e\u8089\u822c\u7684', r'\u8150\u8089\u822c\u7684'),
]

changed = 0
for find, replace in REPLACEMENTS:
    count = src.count(find)
    if count == 0:
        safe = find[:70].encode("unicode_escape").decode("ascii")
        print(f"  WARNING not found: {safe}")
    else:
        src = src.replace(find, replace)
        changed += count
        print(f"  OK x{count}: {find[:50].encode('unicode_escape').decode('ascii')}")

# ── Add missing key: 梦魅凝视 (dream phantom gaze) ───────────────────────────
# Insert after the newly-fixed "Imprisoned" entry
anchor = r'"\u53d7\u5230\u7981\u9522": "Imprisoned",'
new_entry = anchor + '\n    "\\u68a6\\u9b47\\u51dd\\u89c6": "Dream phantom gaze",'
if anchor in src:
    src = src.replace(anchor, new_entry, 1)
    print("  OK: added dream phantom gaze key")
else:
    print("  WARNING: could not find Imprisoned anchor")

# ── Pass 2: curly-quote fixes (must run from file, not -c, to preserve backslashes) ──
PASS2 = [
    # 明心 escaped-quote → curly-quote
    (r' \"\u660e\u5fc3\" ', r' \u201c\u660e\u5fc3\u201d '),
    # 舍身 escaped-quote → curly-quote
    (r' \"\u820d\u8eab\" ', r' \u201c\u820d\u8eab\u201d '),
    # angry gaze: fix chars + curly quotes (5c71→521a, 762b→778b, 523b→5239)
    (
        r' \"\u6012\u76ee\u91d1\u5c71\u762b\u76ee\u89c6\uff0c\u6076\u523b\u5996\u9b54\u7686\u80c6\u88c2\u3002\"',
        r' \u201c\u6012\u76ee\u91d1\u521a\u778b\u76ee\u89c6\uff0c\u6076\u5239\u5996\u9b54\u7686\u80c6\u88c2\u3002\u201d',
    ),
    # 菩提本无树 escaped-quote → curly-quote
    (
        r'\"\u83e9\u63d0\u672c\u65e0\u6811\uff0c\u660e\u955c\u4ea6\u975e\u53f0\"',
        r'\u201c\u83e9\u63d0\u672c\u65e0\u6811\uff0c\u660e\u955c\u4ea6\u975e\u53f0\u201d',
    ),
    # 欲速则不达 escaped-quote → curly-quote
    (r'\"\u6b32\u901f\u5219\u4e0d\u8fbe\u3002\"', r'\u201c\u6b32\u901f\u5219\u4e0d\u8fbe\u3002\u201d'),
]

for find, replace in PASS2:
    count = src.count(find)
    if count == 0:
        safe = find[:60].encode("unicode_escape").decode("ascii")
        print(f"  PASS2 WARNING not found: {safe}")
    else:
        src = src.replace(find, replace)
        changed += count
        print(f"  PASS2 OK x{count}: {find[:40].encode('unicode_escape').decode('ascii')}")

if src == original:
    print("\nNo changes!")
else:
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"\nWrote {TARGET}  ({changed} replacements)")
