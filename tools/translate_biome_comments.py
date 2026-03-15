#!/usr/bin/env python3
"""
translate_biome_comments.py
Replaces Chinese XML comments in Biome/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_biome_comments.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATIONS = {
    # PeachBlossomGarden.xml
    "===================芳草桃源===================": "=================== Peach Blossom Garden ===================",
    " 新Class ": " Custom worker class ",
    "动物密度": "Animal density",
    "植物密度": "Plant density",
    "远行队采摘桃子": "Caravan foraging: peaches",
    " 鱼 ": " Fish ",
    "地砖": "Terrain by fertility",
    "复杂地形生成": "Complex terrain generation",
    "灵脉土地": "Spirit vein terrain",
    "天气": "Weather",
    "依赖仙路核心": "Requires RimImmortal Core",
    "植物": "Plants",
    "原版草": "Vanilla grass",
    "草": "Ferns",
    "仙路联动药草": "RimImmortal Core herbs",
    "树": "Trees",
    "仙路": "RimImmortal",
    "俗世仙工联动": "Living mod trees",
    "原版，提供原木": "Vanilla trees (for wood)",
    "动物": "Animals",
    "原版——猪牛羊等田园动物": "Vanilla — livestock and farm animals",
    "森林狼，少有的捕食动物": "Timber wolf — rare predator",
    "mod": "Mod-added animals",
    "污染地形生物": "Polluted terrain animals",

    # Steps.xml (GenStep scatter)
    " 古修遗迹分布 ": " Ancient cultivator ruins scatter step ",
    " 要散布的粉精物品列表及其权重 ": " Items to scatter and their weights ",
    " 金子放置 10-20 个 ": " Place 10–20 ",
    " 银子放置 50-100 个 ": " Place 50–100 ",
    " 钢材固定放置 25 个 ": " Steel: fixed placement of 25 ",
    " 没有 count 字段，会使用默认的 1-5 个 ": " No count field — uses default 1-5 ",
    " 测试放置建筑 ": " Test: place building ",
    " 物品生成控制参数 ": " Item scatter control parameters ",
    " 已废弃：原本用于控制堆叠数量，现在由每个物品的count字段控制 ":
        " Deprecated: originally controlled stack count; now handled per-item by count field ",
    " 物品之间的最小距离，防止物品过于密集 ": " Minimum distance between items to prevent clustering ",
    " 在指定半径内最多允许放置的同类物品数量 ": " Max items of the same type within the check radius ",
    " 检查同类物品数量时的搜索半径 ": " Search radius when checking item count ",
    " 物品放置成功率（0-1），用于控制稀有度 ": " Item placement chance (0-1) — controls rarity ",
    " 基础散布参数 ": " Base scatter parameters ",
    " 占位符别动，实际使用itemsToScatter ": " Placeholder — do not modify; actual items defined in itemsToScatter ",
    " 是否创建已使用区域，防止其他生成器在此区域生成内容 ": " Whether to mark used area to block other generators ",
    " 是否允许在水域生物群系中生成 ": " Whether generation is allowed in water biomes ",
    " 每个散布位置之间的最小间距 ": " Minimum spacing between scatter positions ",
    " 距离地图边缘的额外禁建距离 ": " Extra no-build distance from map edges ",
    " 这个控制生成总量 ": " Controls total scatter count ",
    " 每10000个地图格子生成的物品数量范围 ": " Items generated per 10,000 map cells ",
    " 在放置物品前清理的区域大小 ": " Area cleared before placing an item ",
    " 地形验证的半径范围 ": " Radius for terrain validation ",
    " 禁止生成的地形类型列表 ": " Terrain types where generation is disallowed ",
    " 浅水区 ": " Shallow water ",
    " 深水区 ": " Deep water ",
    " 沼泽地 ": " Marsh ",
    " 验证器 - 用于确保物品能被正确放置 ": " Validators — ensure items can be placed correctly ",
    " 验证位置是否可建造 ": " Validate whether the location is buildable ",
    " 检查半径 ": " Check radius ",
    " 需要的地基类型：Light=轻型地基 ": " Required affordance: Light = lightweight foundation ",
    " 确保附近没有非自然建筑物 ": " Ensure no non-natural edifices nearby ",
    " 避开特殊物品 ": " Avoid special things ",

    # TWRL_Terrain_Natural.xml
    "粉草坪": "Pink lawn (disabled)",
    "肥沃粉草坪": "Rich pink lawn (disabled)",
    "蓝草坪": "Blue lawn (disabled)",

    # RI_Buildings_Natural.xml
    "白瑶原石": "Mist agate rock (disabled)",
    "古修建筑遗迹——装了仙路才会掉灵石": "Ancient cultivator building ruin — drops spirit crystals if Core is installed",
    "古修路灯遗迹——装了仙路才会掉灵石": "Ancient cultivator lamp ruin — drops spirit crystals if Core is installed",

    # RI_Plants_Wild_Peach.xml
    "芳草桃源植物": "Peach Blossom Garden plants",
    "寸心蕨": "Inch heart fern",
    "紫彩蕨": "Purple fern",
    "骨蕨": "Bone fern",
    "芦荟Aloe Vera": "Aloe Vera",
    "幻金莲Phantom Gold Lotus": "Phantom Gold Lotus",
    "桃树": "Peach tree",

    # RI_Races_Animal_Peach.xml
    " ==============狸力LiLi================ ": " ============== Li Li ================ ",
    "群居动物": "Herd animal",
    "亲昵间隔": "Nuzzle interval",
    "特殊能力": "Special trainables",
    "用的肉": "Uses this meat type",
    " ==============鹿蜀LuShu================ ": " ============== Lu Shu ================ ",
    "产奶": "Milkable",
    "受伤反击": "Manhunter on damage",
    " ==============长右ChangYou================ ": " ============== Chang You ================ ",
    "下蛋": "Lays eggs",
    "旋龟蛋受精": "Xuan turtle egg (fertilized)",
    "旋龟蛋未受精": "Xuan turtle egg (unfertilized)",
    " 移动速度：比普通猫稍微快一点点 ": " Move speed: slightly faster than a domestic cat ",
    " 价值较高，是很稀有的宠物 ": " High market value — a rare pet ",
    "捕食者": "Predator",
    " nuzzleMtbHours 越小，亲昵越频繁。8代表平均每8个游戏小时蹭人一次，会频繁给小人加心情！ ":
        " Lower nuzzleMtbHours = more frequent nuzzling. 8 = once per 8 game hours — boosts mood often! ",
    " 无法训练 ": " Not trainable ",
    " 生命阶段对应的属性变化 ": " Life stage attribute changes ",
    " 借用原版猫的叫声 ": " Reuses vanilla cat sounds ",
    " 动物特有音效和特效 ": " Animal-specific sounds and effects ",
    " 动物的近战攻击方式：抓挠和咬 ": " Animal melee attacks: scratch and bite ",
    " 战斗力评分，较弱，不用担心触发高强度袭击 ": " Combat power: weak — won't trigger high-intensity raids ",
    " 三个生命阶段的贴图设置 (幼体、青少年、成年) ": " Texture settings for three life stages (baby, juvenile, adult) ",
    " 幼体 (Baby) ": " Baby ",
    " 幼崽的称呼 ": " Baby label ",
    " 幼崽体型缩小 ": " Reduced size for baby ",
    " 成年 (Adult) ": " Adult ",
    " ==================== 2. Lei cat 生成与贴图定义 (PawnKindDef) ==================== ":
        " ==================== Lei cat PawnKindDef ==================== ",

    # Drugs/RI_Miragold.xml
    "弭金砂": "Miragold",
    "研究": "Research requirement",
    "弭金砂效果hediff": "Miragold high effect hediff",
    "飘飘欲仙": "Walk upon air (mood thought)",
    "弭金砂化学": "Miragold chemical",
    "弭金砂耐受": "Miragold tolerance",
    "弭金砂依赖hediff": "Miragold addiction hediff",
    "弭金砂戒断心情": "Miragold withdrawal thought",

    # HediffDefs/RI_Hediffs_Misc.xml
    "昏睡": "Tranquilizer hediff",

    # ThoughtDefs
    "丝丝灵雨": "Spiritual radiance rain thought",

    # WeatherDef/RI_PeachFog.xml
    "桃花障": "Peach blossom maze weather",

    # WeatherDef/RI_QiEnergyRain.xml
    "灵光之雨": "Spiritual radiance rain weather",
    " 限制仅在特定生物群系中出现的额外条件 ": " Extra conditions limiting occurrence to specific biomes ",
    " 雾的效果 ": " Fog effect ",
    " 雨的效果 ": " Rain effect ",
    " 同时使用雾和雨的视觉效果 ": " Combined fog and rain visuals ",
    " 降雨因子影响 ": " Rainfall factor influence ",
    " 天空颜色设置 ": " Sky color settings ",

    # ThingDefs_Items/RI_Items_NewDrugs.xml
    "=================药品前置=================": "================= Drug base type =================",
    "服用": "Ingest command",
    "服用中": "Ingest report string",
    "携带分类": "Take group category",
    "安魂汤": "Tranquilizing soup",

    # ThingDefs_Items/RI_Items_RawPlant.xml
    "==================药材前置=================": "================== Herb base type =================",
    "落地音效得改": "TODO: fix drop sound",
    "幻金莲": "Phantom gold lotus resource",
    "==================食材=================": "================== Food ingredients =================",
    "桃子": "Peach",
    "芦荟": "Aloe vera resource",
    "仙桃": "Immortal peach",

    # RecipeDefs/Recipes_Production.xml
    "切割白瑶砖": "Cut mist agate blocks (disabled)",
    "芦荟搓医药": "Make medicine from aloe vera",
    "芦荟搓医药x4": "Make medicine from aloe vera x4",
    "煮安魂汤x1": "Decoct tranquilizing soup x1",
    "煮安魂汤x4": "Decoct tranquilizing soup x4",
}

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')

def translate_comment(m):
    inner = m.group(1)
    if inner in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[inner]}-->"
    stripped = inner.strip()
    if stripped in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[stripped]}-->"
    if CHINESE_RE.search(inner):
        safe = inner.encode("ascii", "replace").decode("ascii")
        print(f"  UNTRANSLATED comment: <!--{safe}-->")
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
    defs_root = os.path.join(REPO, "Biome", "1.6", "Defs")
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
