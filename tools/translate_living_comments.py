#!/usr/bin/env python3
"""
translate_living_comments.py
Replaces Chinese XML comments and inline strings in Living/1.6/Defs with English.
Run from repo root: python tools/translate_living_comments.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# === Comment translations (key = stripped comment inner text) ===
TRANSLATIONS = {
    # HediffDefs/RI_Hediff_Drugs.xml
    " 烟草 ": " Tobacco ",
    " 状态消退速度 ": " Status decay rate ",
    " ==================== 5. 耐受度与成瘾性 (防止报错的支撑文件) ==================== ":
        " ==================== 5. Tolerance and addiction (support file to prevent errors) ==================== ",
    " 即使极难成瘾，环世界依然要求药物必须配套这三个节点，否则会爆红字 ":
        " Even with extremely low addiction chance, RimWorld requires drugs to have these three nodes or errors will be thrown ",

    # SoundDefs/RI_Sound_Misc.xml
    "挥棒子咻一声": "Swing whoosh",
    "劈木头咔一声": "Chop thwack",
    "锯木头声音": "Sawing sound",
    "劈木头声音": "Chopping sound",

    # ThingCategoryDefs/RI_ThingCategories_Living.xml
    "====================================仙路储存====================================":
        "==================================== RimImmortal storage ====================================",
    "================一级分类（已经无了）=====================":
        "================ Top-level categories (removed) =====================",
    "仙路-衣着": "RimImmortal — Apparel",
    "衣冠": "Headwear",
    "====================================仙路原料====================================":
        "==================================== RimImmortal raw materials ====================================",
    "仙路-原料": "RimImmortal — Raw materials",
    "畜牧": "Livestock",
    "药材": "Herbs",
    "土木": "Earth and wood",
    "金石": "Metal and stone",
    "====================================仙路成品====================================":
        "==================================== RimImmortal products ====================================",
    "仙路-成品": "RimImmortal — Products",
    "布帛": "Textiles",

    # WorkGiverDefs/RI_WorkGivers.xml
    "烧制粘土": "Fire clay",
    "挖掘": "Excavate",
    "电饭煲框架，投料work": "Rice cooker framework — fill work",
    "木材加工": "Wood processing",
    "热压原料": "Heat-press raw materials",
    "操作工业钻机": "Operate industrial drill",
    " 使用你刚才写的 C# 类 ": " Use your C# class ",
    " 关键！在这里填入你的工业钻机的 defName ": " Key: fill in the defName of your industrial drill here ",

    # ThingDefs_Misc/RI_Apparel_Various.xml
    "短衫": "Short tunic",
    "直裰": "Zhiduo robe",
    "长绔": "Long trousers",
    "原料": "Materials",
    "小包帕": "Small handkerchief bag",
    "和发型同时显示": "Displays with hairstyle",
    "庄子巾": "Zhuangzi headscarf",

    # ThingDefs_Misc/RI_Apparel_Base.xml
    "布帛菽粟的前置和核心的前置分开":
        "Living mod base separated from Core mod base",
    "===================== 衣服 =====================": "===================== Clothing =====================",
    "服装前置——基础衣服前置，ApparelBase不用改了yyds":
        "Clothing base — inherits from ApparelBase (no changes needed)",
    "贴图": "Texture",
    "储存": "Storage",
    "制作清单": "Crafting requirements",
    "贸易tag": "Trade tag",
    "随机颜色": "Random color",
    "不让npc刷新": "Prevent NPC refresh",
    "服装前置——没有布料皮料，基础服饰":
        "Clothing base — no textile/leather requirement, basic apparel",
    "===================== 帽子 =====================": "===================== Hats =====================",
    "帽子前置——基础帽子": "Hat base — basic hat",
    "服装特性": "Apparel properties",
    "不知道干嘛的": "Unknown purpose",
    "帽子前置——没有布料皮料，基础帽子":
        "Hat base — no textile/leather requirement, basic hat",

    # ThingDefs_Misc/RI_Apparel_Headgear.xml
    "瓦楞帽": "Woven straw hat",
    "帷帽": "Veil hat",
    "三山帽": "Three-peak hat",
    "小冠": "Small crown",
    "嵌金三山帽——没有原料": "Gold-inlaid three-peak hat — no materials required",

    # ThingDefs_Misc/RI_Apparel_Pack.xml
    " ===============背包基础=============== ": " =============== Backpack base =============== ",

    # ThingDefs_Buildings/RI_Buildings_IceBox.xml
    "寒髓冰鉴": "Marrow ice cellar",
    "冒个蓝光": "Emits blue glow",
    "效率为1天消耗1寒髓": "Efficiency: consumes 1 marrow per day",
    "百工解锁": "Unlocked by research",

    # ThingDefs_Buildings/RI_Buildings_Production.xml
    "砖窑": "Brick kiln",
    "烧砖": "Fire bricks",
    "窑炉该干的活": "Kiln work",
    "挖泥坑": "Dig mud pit",
    "电窑炉": "Electric kiln",
    " 中世纪————锯马 ": " Medieval — sawhorse ",
    " 工业————热压机 ": " Industrial — heat press ",
    "可以制作合成纤维，别的能做的得想想": "Can make synthetic fiber; other possible uses TBD",
    "工业钻机": "Industrial drill",
    "不可通过": "Impassable",
    " 更大！ ": " Larger! ",

    # ThingDefs_Buildings/Buildings_Group.xml
    "仙路生产": "RimImmortal production",

    # ThingDefs_Buildings/RI_Buildings_Fermentation.xml
    "蚕箱": "Silkworm box",
    "没有ticker建筑就不会运行": "Building requires ticker to function",
    " 空闲状态 ": " Idle state ",
    " 工作状态 ": " Working state ",
    "产出产物": "Produce output",
    "完成的音效": "Completion sound",
    "工作需要的tick_5天": "Work duration in ticks — 5 days",
    "下雨是否摧毁产物": "Whether rain destroys output",
    "需不需要电力": "Whether power is required",
    "冰蚕箱": "Ice silkworm box",

    # UpdateNews/RI_UpdateNews.xml
    " ======================仙路-俗世仙工 更新信息====================== ":
        " ====================== RimImmortal-Living update info ====================== ",
    " 这里写翻译键，而不是直接写名字 ": " Write translation key here, not the name directly ",
    " 这里也写翻译键 ": " Write translation key here too ",
    " 在这里微调坐标和大小 ": " Fine-tune position and size here ",
    " 距离屏幕左边 ": " Distance from screen left edge ",
    " 距离屏幕顶端 ": " Distance from screen top edge ",
    " 宽度调窄一点 ": " Narrow the width slightly ",
    " 高度调长一点 ": " Increase the height slightly ",

    # JobDefs/RI_Jobs_Work.xml
    "电饭煲框架，投料job": "Rice cooker framework — fill job",
    " ★ 必须与 C# RI_WineBarrelDefOf.FillWineBarrel 变量名一致 ":
        " ★ Must match C# RI_WineBarrelDefOf.FillWineBarrel variable name ",
    " ★ 指向你的 C# JobDriver 类 ": " ★ Points to your C# JobDriver class ",
    " ★ 必须与 C# RI_WineBarrelDefOf.TakeProductFromWineBarrel 变量名一致 ":
        " ★ Must match C# RI_WineBarrelDefOf.TakeProductFromWineBarrel variable name ",

    # ThingDefs_Items/TW_TCT_Resource.xml
    " 压缩木板 ": " High-density board (disabled) ",
    " 木工胶 ": " Wood glue (disabled) ",

    # ThingDefs_Items/RI_Items_Resource_MetalAndStone.xml
    "镔铁": "Damascus iron",
    "乌刚玉": "Black corundum",
    "青砖": "Black bricks",
    "红砖": "Red bricks",
    "寒髓": "Marrow crystal",

    # ThingDefs_Items/RI_Items_Resource_Silk.xml
    "布料啥的前置": "Textile base",
    "丝绸": "Silk",
    "火浣皮": "Fireproof hide",
    "冰蚕丝": "Ice silkworm thread",
    "金丝": "Gold thread",
    "银丝": "Silver thread",

    # ThingDefs_Items/RI_Items_SilkResource.xml
    "蚕卵": "Silkworm eggs",
    "冰蚕卵": "Ice silkworm eggs",
    "蚕茧": "Silk cocoon",
    "冰蚕茧": "Ice silk cocoon",
    "桑叶": "Mulberry leaves",

    # ThingDefs_Items/RI_Items_Resource_WoodAndMud.xml
    "檀木": "Sandalwood",
    "竹子": "Bamboo",
    "玄铁木": "Ironwood",
    "苍血竹": "Blood bamboo",
    "泥土": "Mud",
    " 薄木材 ": " Thin wood ",
    " 胶合板 ": " Plywood ",
    "真空": "Vacuum",

    # ThingDefs_Items/RI_Items_Cigarette.xml
    " ==================== 1. 化学物质定义 ==================== ":
        " ==================== 1. Chemical substance definition ==================== ",
    " 必须定义一个专属的化学物质，防止它和原版大麻烟的耐受度混淆 ":
        " Must define a unique chemical to prevent tolerance overlap with vanilla smokeleaf ",
    "需求": "Requirements",
    " 云华烟 ": " Cloud blossom cigarette ",
    " 你的香烟贴图路径，建议画一个红色的经典烟盒或者单根香烟 ":
        " Cigarette texture path; suggest a red classic cigarette box or single cigarette ",
    " 【超高价格】原版大麻烟价值是 11，这里设为 85，一包堪比高级零部件 ":
        " [Very high price] Vanilla smokeleaf costs 11; set to 85 here — one pack rivals advanced components ",
    "价值多少贡献点": "Contribution value",
    " 易燃 ": " Flammable ",
    " 作为娱乐药物使用 ": " Used as recreational drug ",
    " 极高的娱乐值补充 (0.9 代表抽一根几乎能补满娱乐条) ":
        " Very high recreation boost (0.9 = nearly fills recreation bar per cigarette) ",
    " 1. 抽完给 High 的状态 ": " 1. Gives high state after use ",
    " 2. 给一点点微乎其微的耐受度 ": " 2. Adds minimal tolerance ",
    " 【极低成瘾性】原版大麻是 0.02，这里是 0.005 (0.5%的概率)，而且需要非常高的耐受度才会触发成瘾判定 ":
        " [Extremely low addiction] Vanilla smokeleaf is 0.02; this is 0.005 (0.5% chance),"
        " requires very high tolerance to trigger ",
    " ==================== 4. 抽烟后的心情加成 (Thought) ==================== ":
        " ==================== 4. Post-smoke mood bonus (Thought) ==================== ",
    "戒断心情": "Withdrawal thought",

    # ThingDefs_Items/RI_Items_MaoZi.xml
    " 御贡酒 ": " Royal tribute wine (disabled) ",
    " 记得准备贴图 ": " Remember to prepare the texture ",
    " 高度酒易燃 ": " High-proof alcohol is flammable ",
    " 提供大量娱乐 (啤酒只有 0.17) ": " Provides large recreation boost (beer is only 0.17) ",
    " 强劲：一瓶顶三瓶啤酒 (啤酒 0.15) ": " Strong: one bottle equals three beers (beer is 0.15) ",
    " 成瘾性略高于啤酒 ": " Addiction rate slightly higher than beer ",

    # RecipeDefs/RI_Recipes_Wood.xml
    "劈开原木，用到近战1级": "Chop log — requires Melee 1",
    "锯木头Base": "Saw wood base",
    "描述": "Description",
    "锯开原木": "Saw off log",
    "锯开原木x4": "Saw off log x4",
    "锯开檀木": "Saw off sandalwood",
    "锯开檀木x4": "Saw off sandalwood x4",
    "锯开玄铁木": "Saw off ironwood",
    "锯开玄铁木x4": "Saw off ironwood x4",

    # RecipeDefs/RI_Recipes_Silk.xml
    "金丝银丝Base": "Gold/silver thread base",
    "丝绸Base": "Silk base",
    "织造丝绸": "Weave silk",
    "织造冰蚕丝": "Weave ice silkworm thread",
    "织造丝绸 x4": "Weave silk x4",
    "织造冰蚕丝 x4": "Weave ice silkworm thread x4",
    "捻制金丝": "Spin gold thread",
    "捻制银丝": "Spin silver thread",
    "熔炼Base": "Smelting base",
    "金丝熔炼回金子": "Smelt gold thread back to gold",
    "银丝熔炼回银子": "Smelt silver thread back to silver",

    # RecipeDefs/RI_Recipes_MakeStuff.xml
    "挖泥": "Dig mud",
    "学不到东西": "No skill gain",
    "挖泥 x4": "Dig mud x4",
    "烧砖Base": "Fire brick base",
    "烧制青砖": "Fire black bricks",
    "烧制红砖": "Fire red bricks",
    "把铁木整成钢铁？": "Convert ironwood to steel?",
    "锻打镔铁": "Forge Damascus iron",
    "锻打镔铁x4": "Forge Damascus iron x4",
    "培养蚕Cultivate more silkworm": "Cultivate silkworms",
    "培养冰蚕Cultivate more silkworm": "Cultivate ice silkworms",
    "======================热压机配方======================": "====================== Heat press recipes ======================",
    "热压Base": "Heat press base",
    "制作合成纤维": "Make synthetic fiber",
    "制作纤维x4": "Make synthetic fiber x4",
    "木板制作胶合板": "Make plywood from planks",
    "木板制作胶合板 x4": "Make plywood from planks x4",
    "竹子制作胶合板": "Make plywood from bamboo",
    "竹子制作胶合板 x4": "Make plywood from bamboo x4",
    "铁木热压钢铁": "Heat-press ironwood to steel",
    "铁木热压钢铁 x4": "Heat-press ironwood to steel x4",

    # ResearchProjectDefs
    "=============================== 部落到中世纪的科技 ===================================":
        "=============================== Tribal to Medieval technology ===================================",
    "天工开物": "Heavenly crafts",
    "纺织": "Textile weaving",
    "布衣裁缝": "Cloth tailoring",
    "王朝锦衣": "Dynasty silk apparel",
    "百工": "Industrial crafts",
    "============================中世纪============================":
        "============================ Medieval ============================",
    "奇花异木": "Exotic flowers and trees",
    "锻钢": "Steel forging",
    "============================电力时代============================":
        "============================ Industrial age ============================",
    "电力学": "Electrology",
    " 泰南，你好贴心 ": " Thanks for thinking of everything, Tynan ",

    # TerrainDefs
    "地砖": "Floor tiles",
    "石板": "Stone tiles",

    # ThingDefs_Plants/RI_Plants_Trees.xml
    "毛竹": "Mao bamboo",
    "檀木树": "Sandalwood tree",
    "苍血竹": "Blood bamboo tree",
    "铁木树": "Ironwood tree",
    "桑树——收获得到桑叶": "Mulberry tree — harvest yields mulberry leaves",
    "描述超链接": "Description hyperlinks",

    # ThingDefs_Plants/RI_Plants_Decorative.xml
    "==================传统花卉==================": "================== Traditional flowers ==================",
    "花卉前置": "Flower base",
    "兰花": "Orchid",
    "种植特点": "Planting notes",
    "水仙": "Narcissus",
    "牡丹": "Peony",
    "菊花": "Chrysanthemum",

    # ThingDefs_Races/RI_Animal_Basic.xml
    " =========================火鼠============================= ":
        " ========================= Fire rat ============================= ",
    " ==========================天狗============================ ":
        " ========================== Sky hound ============================ ",
}

# === Direct inline replacements (applied to raw file content, for strings
#     inside large commented-out XML blocks) ===
INLINE_REPLACEMENTS = [
    # RI_Recipes_Wood.xml — commented-out wood glue/plywood recipes
    ("<label>熬制木工胶</label>", "<label>brew wood glue</label>"),
    ("<description>用动物皮来熬制木工胶，比较缓慢。</description>",
     "<description>Brew wood glue from leather. Slow process.</description>"),
    ("<jobString>正在熬制木工胶。</jobString>",
     "<jobString>brewing wood glue</jobString>"),
    ("<label>熬制木工胶 x5</label>", "<label>brew wood glue x5</label>"),
    ("<label>提炼木工胶</label>", "<label>refine wood glue</label>"),
    ("<description>随着化工业的发展，发明了用中性胺和动物皮制作木工胶的技术，"
     "这种工艺略微复杂，但是产量得到了飞跃式的进步。</description>",
     "<description>With the development of the chemical industry, a technique for making"
     " wood glue from neutroamine and leather was invented."
     " This process is slightly complex, but yields dramatically more output.</description>"),
    ("<jobString>正在提炼木工胶。</jobString>",
     "<jobString>refining wood glue</jobString>"),
    ("<label>提炼木工胶 x5</label>", "<label>refine wood glue x5</label>"),
    ("<label>热压胶合板</label>", "<label>heat-press plywood</label>"),
    ("<description>通过工业热压机，可以让胶合板制作效率变得更高，高压高温技术让木工胶的消耗更少了，"
     "制作速度也更快。</description>",
     "<description>Industrial hot-pressing equipment greatly increases plywood production efficiency."
     " High heat and pressure reduce wood glue consumption and speed up the process.</description>"),
    ("<jobString>正在热压胶合板。</jobString>",
     "<jobString>heat-pressing plywood</jobString>"),
    ("<label>热压胶合板 x5</label>", "<label>heat-press plywood x5</label>"),
    ("<label>压制压缩木板</label>", "<label>compress high-density board</label>"),
    ("<label>压制压缩木板 x5</label>", "<label>compress high-density board x5</label>"),

    # TW_TCT_Resource.xml — commented-out high-density board resource
    ("<label>压缩木板</label>", "<label>high-density board</label>"),
    ("<description>将原木以高压和高温蒸汽处理之后的压缩木板。这种材料显著提高了木材的密度和阻燃性，"
     "也比较美观，非常适合制作家具。</description>",
     "<description>A compressed board produced by treating raw logs with high-pressure steam."
     " This material significantly increases wood density and fire resistance,"
     " while also being aesthetically pleasing — ideal for furniture crafting.</description>"),
    ("<stuffAdjective>压缩木板</stuffAdjective>",
     "<stuffAdjective>high-density board</stuffAdjective>"),
    ("<label>木工胶</label>", "<label>wood glue</label>"),

    # RI_Buildings_Production.xml — commented-out table saw
    ("<label>台锯</label>", "<label>table saw</label>"),
    ("<description>一种使用圆形锯片的机床，可以快速有效地将原木切割成想要的形状。</description>",
     "<description>A machine tool using a circular saw blade, capable of quickly and efficiently"
     " cutting raw logs into desired shapes.</description>"),
]

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')
COMMENT_RE = re.compile(r'<!--(.*?)-->', re.DOTALL)


def translate_comment(m):
    inner = m.group(1)
    if inner in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[inner]}-->"
    stripped = inner.strip()
    if stripped in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[stripped]}-->"
    if CHINESE_RE.search(inner):
        safe = inner.encode("ascii", "replace").decode("ascii")
        # Only print first 80 chars to avoid flooding output with large blocks
        print(f"  UNTRANSLATED comment: <!--{safe[:80]}{'...' if len(safe)>80 else ''}-->")
    return m.group(0)


def process_file(path):
    with open(path, encoding="utf-8") as f:
        original = f.read()
    result = original

    # Pass 1: translate standard XML developer comments
    result = COMMENT_RE.sub(translate_comment, result)

    # Pass 2: direct inline replacements for strings inside commented-out XML blocks
    for old, new in INLINE_REPLACEMENTS:
        result = result.replace(old, new)

    if result != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main():
    defs_root = os.path.join(REPO, "Living", "1.6", "Defs")
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
