#!/usr/bin/env python3
"""
translate_fiveelements_comments.py
Replaces Chinese XML comments in FiveElements/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_fiveelements_comments.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATIONS = {
    # ===== AbilityDefs/RI_Route_FiveElement.xml =====
    "火行法门": "Fire element technique",
    "木行法门": "Wood element technique",
    "土行法门": "Earth element technique",
    "凝气": "Qi condensation",
    "固基": "Foundation building",
    "化丹": "Core formation",
    "结丹": "Golden core",
    "灵丹": "Spirit core",
    "化神": "Deity transformation",
    "跳过化神": "Skip deity transformation",
    "元婴": "Nascent soul",
    "大成": "Great completion",

    # ===== AbilityDefs/RI_Abilities_FireElement.xml =====
    " 离火 ": " Departing flame cultivation ",
    " TODO 下面需要处理 ": " TODO: handle below ",
    "触发特效": "Trigger effect",
    " 心炎 ": " Life fire activation ",
    " 吹火 ": " Flame breath ",
    "冷却": "Cooldown",
    " 炽飞雀 ": " Blazing sparrow ",
    " 炽飞雀小 ": " Blazing sparrow (small) ",
    " 焚绝 ": " Burning annihilation ",
    " 声音 ": " Sound ",
    " 烈日炎威 ": " Blazing sun majestic flame ",
    "冷却时间": "Cooldown time",
    " 追焰 ": " Chasing flame ",
    " 乾阳焱火决 ": " Qianyang blazing flame technique ",

    # ===== AbilityDefs/RI_Abilities_EarthElement.xml =====
    " 土行法门 ": " Earth element technique ",
    " 凝气境界——坤土 ": " Qi condensation — Kun Earth cultivation ",
    "技能准备特效": "Skill readying effect",
    " 凝气境界——乾元生柱 ": " Qi condensation — earth spirit column ",
    "1小时": "1-hour cooldown",
    " 化丹境界——石甲护身 ": " Core formation — stone armor ",
    " 结丹境界——岩碎 ": " Golden core — shattered rock ",
    " 结丹境界——土壁 ": " Golden core — earth wall ",
    " 灵丹境界——陷地吞沙 ": " Spirit core — sand trap ",
    "4小时冷却": "4-hour cooldown",
    "婴后": "Post-Nascent soul",
    " 灵丹境界——石塔镇界 ": " Spirit core — guardian stone tower ",
    "24小时一个": "One per 24-hour cooldown",
    " 元婴境界——乾坤震地 ": " Nascent soul — earth-shaking quake ",
    " 合体境界大招——八荒磐岩 ": " Fusion realm ultimate — eight wastes bedrock ",

    # ===== AbilityDefs/RI_Abilities_WoodElement.xml =====
    " 木行法门 ": " Wood element technique ",
    "凝气境界——巽木": "Qi condensation — Xun Wood cultivation",
    "读条特效": "Cast bar effect",
    "光圈": "Aura",
    "固基境界——春生": "Foundation building — spring growth",
    "冷却12小时": "12-hour cooldown",
    " 生机予夺 ": " Vitality absorption ",
    " 选中一个范围内的植物，摧毁它们以获取生命力 ":
        " Target plants in range and destroy them to gain vitality ",
    " TODO 替换声音 ": " TODO: replace sound ",
    " 每100%生长的植物转化为X点生机 ":
        " Each 100% grown plant converts to X points of vitality ",
    " 摧毁植物 ": " Destroy plants ",
    " 半径 ": " Radius ",
    " 特效Mote ": " Visual effect mote ",
    " 化丹——结草缚藤 ": " Core formation — verdant bind ",
    " 选中一个范围内的植物，让它们转变为陷阱，地雷 ":
        " Target plants in range, transform them into traps and mines ",
    " 选中一个范围内的植物，让它们变成炮台 ":
        " Target plants in range, transform them into turrets ",
    " 默认类型的生物 ": " Default creature type ",
    " 树对应的生物 ": " Creature corresponding to trees ",
    " 特定植物对应的生物 ": " Creature types for specific plants ",
    "生机草": "Vitality grass",
    "生机灌木": "Vitality bush",
    "生机海芋": "Vitality alocasia",
    "绞杀荆棘": "Strangle-thorn",
    "龙刺": "Agave-spike",
    " 结丹——草木列阵 ": " Golden core — garden army ",
    "莓果": "Berry-shooter",
    "刺球": "Cactus-spitter",
    "玉米": "Corn-cannon",
    " 灵丹——森灵护卫 ": " Spirit core — forest guardian ",
    " 选中一个范围内的植物，让它们变成可移动守卫 ":
        " Target plants in range, transform them into mobile guards ",
    " 选中一颗足年的大树，让它化生成精，它的生存时间有限，但是存活时间越长，力量越强，(两个Hediff，\"有限的生命\"，\"成长\") ":
        " Target a fully-grown tree and transform it into a verdant creature."
        " Its lifespan is limited, but it grows stronger over time."
        " (Two hediffs: Limited life + Verdant growth) ",
    " 回复部分灵气 ": " Restores partial Qi energy ",
    " 默认类型的生物——树精 ": " Default creature type — verdant creature ",
    " 添加Hediff ": " Add hediff ",
    " 化神—— 生机嫁接 ": " Deity transformation — vitality graft ",
    " 选中一个pawn，延长它有限的生命 ": " Target a pawn to extend its limited lifespan ",
    " 选中一个范围内树精，将生命力注入到它们身上,注入的生命将由范围内的单位分担 ":
        " Target verdant creatures in range and inject vitality;"
        " the cost is shared among units in range ",
    " 最小生命值供给 ": " Minimum vitality supply ",
    " 生机乘数 ": " Vitality multiplier ",
    " 生机消耗百分比 ": " Vitality consumption percentage ",
    "<!--触发特效-->": "Trigger effect",
    " TODO 寄生种子(暂时不做) ": " TODO: Parasitic seed (not yet implemented) ",
    " 选中一个无法反抗的pawn，注入一个种子，这个种子每隔一段时间都会收取生命力给主人 ":
        " Target a helpless pawn and inject a seed;"
        " the seed periodically drains vitality and gives it to the caster ",
    " TODO 开花(暂时不做) ": " TODO: Blooming (not yet implemented) ",
    " 选中一个被寄生时间足够长的单位，他们的头部会开出一个巨大的花朵，目标的心智会被取代(类似心偶)，(两个Hediff，\"有限的生命\"，\"成长\") ":
        " Target a pawn parasitized long enough; a massive flower blooms from their head,"
        " replacing their mind (like a mindscrew). (Two hediffs: Limited life + Verdant growth) ",

    # ===== HediffDefs/RI_Hediffs_FireElement.xml =====
    "火行Base": "Fire element base",
    "离火功法": "Fire cultivation method",
    " 焚心 ": " Life fire ",
    "附加特效": "Additional visual effects",
    "一段时间后消失": "Disappears after a time",
    "眼睛发光": "Eyes glow",
    " 炎威 ": " Majestic flame ",
    " 乾阳焱火决 自身 ": " Qianyang blazing flame technique (self) ",
    " 乾阳焱火决 目标 心火焚烧 ": " Qianyang blazing flame technique (target) — soul burning ",
    " TODO 替换 ": " TODO: replace ",

    # ===== HediffDefs/RI_Hediffs_WoodElement.xml =====
    " 木行Base ": " Wood element base ",
    "巽木功法": "Wood cultivation method",
    " 生机滋养 ": " Vitality nourishment ",
    " 揽草木之生机，滋养己身。引生发之曲直，增其威势。":
        " Absorb the vitality of plants to nourish oneself;"
        " harness the power of growth and expansion to enhance strength.",
    "毒性抵抗系数": "Toxic resistance coefficient",
    "携带": "Carry capacity",
    "种植速度": "Plant work speed",
    " TODO 添加更多层数 ": " TODO: add more tiers ",
    "=============================树灵专有hediff=============================":
        "============================= Verdant creature hediffs =============================",
    " 有限生机 ": " Limited life ",
    " 树灵得生机造化而诞生，它们的存在会逐渐消耗有限的生机，直到自然死亡。 ":
        " Verdant creatures are born from the essence of life."
        " Their existence gradually consumes this limited vitality until they naturally perish. ",
    "聪明动物": "Smart animal",
    " 初始存活时间 ": " Initial survival time ",
    " 最长存活时间 ": " Max survival time ",
    " 耗尽 ": " Exhaust ",
    " 充盈 ": " Replete ",
    " 枝繁叶茂 ": " Verdant growth ",
    " 树灵得生机造化而诞生，它们将在短暂的生命中肆意生长，变得越来越强。 ":
        " Verdant creatures are born from the essence of life."
        " In their brief lifespan, they grow wildly and become increasingly powerful. ",
    " 嫩芽 ": " Sprout ",
    " 幼苗 ": " Seedling ",
    " 新木 ": " Sapling ",
    " 葱郁 ": " Lush ",
    " 苍翠 ": " Verdant ",
    " TODO 补充更多 ": " TODO: add more stages ",
    "伤害效果": "Damage effects",
    "荆棘缠身": "Thorn entangled",
    " 持续时间约 16.6 秒 ": " Duration approx. 16.6 seconds ",
    " 移动速度降低50% ": " Move speed reduced 50% ",

    # ===== HediffDefs/RI_Hediffs_EarthElement.xml =====
    "土行Base": "Earth element base",
    "坤土功法": "Earth cultivation method",
    " 石甲 ": " Stone armor ",
    " 碎岩 ": " Shattered rock ",
    " 镇岳盾 ": " World-sealing shield ",
    "不会自动恢复": "Does not auto-regenerate",
    "一出石塔范围就开始疯狂掉": "Drains rapidly when out of tower range",
    " 石化 ": " Petrified ",

    # ===== ResearchProjectDefs/RI_ResearchProjects.xml =====
    "=============================== 五行科技树 ===================================":
        "=============================== Five Elements tech tree ===================================",
    "=====离火======": "===== Fire element =====",
    "=====巽木======": "===== Wood element =====",
    "=====坤土======": "===== Earth element =====",

    # ===== ThingDefs_Buildings/Buildings_Security.xml =====
    "==================== 木行植物陷阱 ======================== ":
        "==================== Wood element plant traps ======================== ",

    # ===== ThingDefs_Buildings/Buildings_Security_Turrets.xml =====
    "==================== 木行植物炮台 ======================== ":
        "==================== Wood element plant turrets ======================== ",
    "玉米炮": "Corn-cannon turret",
    "玉米炮——枪": "Corn-cannon — gun",
    "莓果塔": "Berry-shooter turret",
    "莓果塔-枪": "Berry-shooter — gun",
    "莓果塔-子弹": "Berry-shooter — bullet",
    "多棱刺球": "Cactus-spitter turret",
    "多棱刺球-枪": "Cactus-spitter — gun",
    "多棱刺球-子弹": "Cactus-spitter — bullet",

    # ===== ThingDefs_Buildings/Buildings_Structure.xml =====
    " 乾元柱 ": " Earth column ",
    "支撑范围": "Support radius",
    "土壁": "Earth wall",
    "可建造土壁": "Buildable earth wall",
    "原料": "Materials",
    "研究完可以造，需要Living": "Unlocked by research; requires Living mod",
    " 镇岳塔 ": " Guardian stone tower ",
    "显示范围": "Display radius",
    "流沙陷阱": "Quicksand trap",
    "持续2小时": "Duration: 2 hours",

    # ===== ThingDefs_Misc/RI_Weapon_FiveElements.xml =====
    "三品——燕火刀（依赖炼器）": "Third-rate — Yan fire blade (requires Forge)",
    "图标贴图": "Icon texture",
    "标签": "Tags",
    "武器攻击效果": "Weapon attack effects",
    "三品——衡元棍（依赖炼器）": "Third-rate — HengYuan quarterstaff (requires Forge)",
    "依赖炼器": "Requires Forge mod",
    "三品——见血封喉（依赖炼器）": "Third-rate — upas blood (requires Forge)",
    " 按体型缩放 ": " Scales by body size ",

    # ===== ThingDefs_Plants/RI_Plants_WoodElement.xml =====
    "====================================== 木行制造的植物 ======================================== ":
        "====================================== Wood element created plants ======================================== ",
    "收获得到草药": "Harvest yields herbal medicine",

    # ===== ThingDefs_Races/Races_Animal_Special.xml =====
    "树精前置": "Verdant creature base",
    "超链接": "Hyperlinks",
    "无性别": "No gender",
    "虫子Ai": "Insect AI",
    "DLC动物能力": "DLC animal abilities",
    "给予hediff": "Grants hediff",
    "树精物种前置": "Verdant creature kind base",
    " 森林护卫 Verdant guard ": " Verdant guard ",
    "由一般的树木转变而成": "Transformed from ordinary trees",
    "屠宰产物": "Butcher products",
    " 青冥树灵 QingMing dryad ": " QingMing dryad ",
    "由青冥树转变而成": "Transformed from QingMing trees",

    # ===== ThingDefs_Items/RI_Items_Books.xml =====
    " ================================== 火行法门书 ====================================":
        " ================================== Fire element technique book ====================================",
    " ================================== 木行法门书 ====================================":
        " ================================== Wood element technique book ====================================",
    " ================================== 土行法门书 ====================================":
        " ================================== Earth element technique book ====================================",

    # ===== DamageDefs/RI_Damages_Misc.xml =====
    "荆棘伤害": "Thorn damage",
    " 下面定义的 Hediff ": " Hediff defined below ",

    # ===== Effects/Effecter_Fire.xml =====
    " 测试特效 ": " Test visual effect ",
    "只需要一次": "Only once",
    "顺时针旋转速度，360是每秒一圈，负是逆时针":
        "Clockwise rotation speed — 360 = one full turn per second, negative = counter-clockwise",
    "循环播放的间隔": "Loop interval",
    "技能选中特效——火行——离火": "Skill select effect — Fire element — Departing flame",

    # ===== Effects/RI_Effecter_Wood.xml =====
    "技能选中特效——木行——巽木": "Skill select effect — Wood element — Xun Wood cultivation",
    "技能选中特效——木行——春生": "Skill select effect — Wood element — Spring growth",
    "技能选中特效——木行——生机嫁接": "Skill select effect — Wood element — Vitality graft",
    "生成植物特效": "Plant generation effect",
    "抽取生机特效": "Vitality extraction effect",

    # ===== Effects/RI_Effecter_Earth.xml =====
    "技能选中特效——土行——坤土": "Skill select effect — Earth element — Kun Earth cultivation",
    "技能选中特效——土行——基础": "Skill select effect — Earth element — basic",
    "技能选中特效——土行——地震": "Skill select effect — Earth element — earthquake",
    "技能选中特效——土行——土之领域": "Skill select effect — Earth element — Earth domain",

    # ===== SoundDefs =====
    "植物生长": "Plant growth",
    "火球A": "Fireball A",
    "火球B": "Fireball B",
    "火球C": "Fireball C",
    "火焰启动": "Flame activation",
    "火行大招A": "Fire element ultimate A",
    "岩石冲击": "Rock impact",

    # ===== ThingDefs_Items/Gun_Test.xml =====
    " 测试炽飞雀用的枪 ": " Test gun for the blazing sparrow ",
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
    defs_root = os.path.join(REPO, "FiveElements", "1.6", "Defs")
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
