#!/usr/bin/env python3
"""
translate_furniture_comments.py
Replaces Chinese XML comments in Furniture/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_furniture_comments.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Map of Chinese comment text → English replacement (comment text only, no <!-- -->)
TRANSLATIONS = {
    # ResearchProjects.xml
    "=============================== 部落到中世纪的科技 ===================================":
        "=============================== Tribal to Medieval Technology ===================================",
    "照明": "Lighting",
    "地砖铺设": "Floor tiles",
    "榫卯": "Mortise and tenon",
    "节日家具": "Festival furniture",
    "明式家具": "Ming-style furniture",
    "王朝家具": "Dynasty furniture",
    "现代中式家具": "Modern Chinese furniture",

    # ResearchTabs.xml
    "雕梁画栋特有介绍": "RimImmortal-Furniture research tab",
    " 仙路生活系列科技树，如果没有装核心，就用这个，装了就patch核心 ":
        " RimImmortal Living tech tree — used standalone; patched if Core is installed ",

    # Floors
    "太阳纹地砖": "Sun-patterned tile",
    "红砖": "Red brick",
    "青砖": "Black brick",
    "交错细墁": "Staggered fine tile",
    "雕梁画栋地砖——石块类的": "RimImmortal floor tiles (stone types)",
    "石片铺地": "Flake floor",
    "方砖斜墁": "Diagonal-laid square tile",
    "细墁地砖": "Fine plastered floor tile",
    "冰裂纹石砖": "Ice-crack stone brick",
    "檀木地板 需要锦衣玉食": "Sandalwood floor (requires Living mod)",
    "竹地板 需要锦衣玉食": "Bamboo plank floor (requires Living mod)",

    # Buildings_Art
    "修仙小雕塑": "Cultivation small sculpture (disabled)",

    # Buildings_Group
    "家具group": "Furniture designation group",

    # RI_Buildings_Base
    "===========仙路最基础的家具base===========": "=========== RimImmortal furniture base ===========",
    "明朝家具base": "Ming-style furniture base",
    " 明朝桌子base ": " Ming-style table base ",
    "仙路——床base": "RimImmortal — bed base",
    "明朝床base": "Ming-style bed base",
    "地砖装饰基础": "Floor tile decoration base",
    "地面装饰层": "Floor decoration layer",
    "地板装饰下拉栏": "Floor decoration dropdown",
    "======================= 装饰基础 ==============================":
        "======================= Decoration base ==============================",
    "明朝装饰": "Ming-style decoration",
    "节日装饰": "Festival decoration",
    "现代餐厅装饰": "Modern restaurant decoration",

    # RI_Buildings_Decoration
    "======================= 餐厅装饰 ==============================":
        "======================= Restaurant decorations ==============================",
    "吊柜": "Wall cupboard",
    "======================厨房装饰======================":
        "====================== Kitchen decorations ======================",
    "厨具架": "Cooking tool rack",
    "原木砧板": "Log cutting board",
    "酒坛": "Wine jars",
    "碗堆": "Stack of bowls",
    "瓶瓶罐罐": "Jars and bottles",
    "======================节日装饰======================":
        "====================== Festival decorations ======================",
    "年红": "Red paper (Spring Festival)",
    "灯笼（装饰）": "Red lantern (decoration)",
    "灯笼串（装饰）": "Lantern string (decoration)",
    "干辣椒": "Dry chili",
    "干玉米": "Dry corn",
    "======================= 现代餐厅装饰 ==============================":
        "======================= Modern restaurant decorations ==============================",
    "现代碗柜": "Modern wall cupboard",
    "抽油烟机": "Kitchen hood",
    "水槽": "Kitchen sink",

    # FloorTileDecoration
    "======================= 地板装饰 ==============================":
        "======================= Floor tile decorations ==============================",
    "地板装饰": "Floor decoration dropdown",
    "莲花纹铺地": "Lotus pattern tile",
    "寿字纹铺地": "Longevity pattern tile",
    "太极纹铺地": "Tai-chi pattern tile",
    "花园铺地": "Garden pattern tile",

    # Furniture_Ming
    "================================明式家具================================":
        "================================ Ming-style furniture ================================",
    "杌凳": "Square stool",
    "坐墩": "Drum stool",
    "条凳": "Long bench",
    "酒桌（1x2）": "Basic table (1x2)",
    "画案（2x3）": "Painting table (2x3)",
    "八仙桌（2x2）": "Eight immortal table (2x2)",
    "月牙桌（1x1）": "Half-round table (1x1)",
    "围屏": "Folding screen",
    "三层架格": "Book shelf",
    "四件柜": "Large cabinet",
    "罗汉床": "Arhat bed",
    "架子床": "Double shelf bed",
    "多层贴图要加": "Requires multi-layer texture comp",
    "多层贴图": "Multi-layer textures",

    # Lantern
    "灯笼": "Red lantern (lit)",
    "现代灯笼": "Modern red lantern (electric)",

    # Lighting
    "明朝灯具Base": "Ming-style lighting base",
    "灯具，没有明火的": "Lamps without open flames",
    "镂空罩灯": "Hood lamp",
    "宫女侍奉灯": "Palace maid lamp",
    "==========================================烛台类==========================================":
        "========================================== Candlesticks ==========================================",
    "烛台一类": "Candlestick group",
    "两种低级的": "Basic types",
    "小烛台": "Small candlestick",
    "花口烛台": "Floral candlestick",
    "高级一点的": "Higher-tier types",
    "莲座烛台": "Lotus pedestal candlestick",
    "立杯烛台": "Goblet-style candlestick",
    "长枝灯台": "Long-branched candlestick",
    "兽首灯台": "Beast-head candlestick",
    "更加高级一点的": "Premium types",
    "辟邪烛台": "Lion-shaped candlestick",
}

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')

def translate_comment(m):
    inner = m.group(1)
    # Try exact match first
    if inner in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[inner]}-->"
    # Try stripped
    stripped = inner.strip()
    if stripped in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[stripped]}-->"
    # If still has Chinese, flag it
    if CHINESE_RE.search(inner):
        print(f"  UNTRANSLATED comment: <!--{inner}-->")
    return m.group(0)

COMMENT_RE = re.compile(r'<!--(.*?)-->', re.DOTALL)

def process_file(path):
    with open(path, encoding="utf-8") as f:
        original = f.read()
    result = COMMENT_RE.sub(translate_comment, original)
    if result != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False

def main():
    defs_root = os.path.join(REPO, "Furniture", "1.6", "Defs")
    changed = 0
    for root, dirs, files in os.walk(defs_root):
        dirs.sort()
        for fname in sorted(files):
            if not fname.endswith(".xml"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, REPO).replace("\\", "/")
            if process_file(fpath):
                print(f"  Updated: {rel}")
                changed += 1
    print(f"\nDone. {changed} files updated.")

if __name__ == "__main__":
    main()
