#!/usr/bin/env python3
"""
translate_forge.py
Replaces Chinese XML comments and inline text in Forge/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_forge.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATIONS = {
    # === TraderDefs/RI_Talisman_Caravan_BlindBox.xml ===
    "盲盒": "Blind Box",
    "盲盒的商队tag": "Blind box caravan tag",
    "50%概率出现罗盘": "50% probability of compass appearing",
    "10%概率出现古修罗盘": "10% probability of ancient cultivator compass appearing",
    "基础材料": "Basic materials",

    # === ResearchProjectDefs/RI_ResearchProjects.xml ===
    "=============================== 部落到中世纪的科技 ===================================": "Tribal to Medieval Technology",
    "简易假肢": "Simple prosthetics",
    "基础法宝合成": "Basic talisman synthesis",
    "低级修士兵器": "Low-grade cultivator weapons",
    "庚钢合成技术": "Geng-steel synthesis technology",
    "神机造物": "Divine machinery creation",
    "低阶灵械傀儡": "Low-tier spirit-mechanical golem",
    "造化医典": "Transformation medicine compendium",
    "现代化修炼设施": "Modernized cultivation facilities",
    "逆生技术突破": "Retrogenesis technology breakthrough",
    "=============================== 工业时期科技 ===================================": "Industrial Era Technology",
    "古修风格复原": "Ancient cultivator style restoration",
    "炼器宗师": "Forging grandmaster",
    "灵气军事学": "Qi military science",

    # === RecipeDefs/RI_Recipes_CopyBook.xml ===
    "这是个模板，所有的抄书逻辑都是根据这个生成的": "This is a template; all book-copying logic is generated from this",
    "别手贱，如果没有ingredients会报错": "Don't touch — it will error if there are no ingredients",

    # === RecipeDefs/RI_Recipes_Talisman.xml ===
    "低阶法宝前置": "Low-tier talisman prerequisite",
    "中阶法宝前置": "Mid-tier talisman prerequisite",
    "高阶法宝前置": "High-tier talisman prerequisite",
    "玉如意": "Jade Ruyi",
    "硬币吊坠": "Coin Pendant",
    "象牙吊坠": "Ivory Pendant",
    "毒铃": "Toxic Bell",
    "令牌": "Token",
    "==================================二品==================================": "Grade 2",
    "储物袋": "Storage Bag",
    "聚石塔": "Stone-Gathering Tower",
    "风戒": "Wind Ring",
    "纳火珠": "Fire-Catching Pearl",
    "青囊葫芦": "Herb Gourd",
    "==================================一品==================================": "Grade 1",
    "紫金葫芦": "Purple-Gold Gourd",
    "金钵": "Golden Bowl",
    "白玉瓶": "White Jade Vase",
    "玲珑塔": "Exquisite Pagoda",
    "乾坤袋": "Heaven-Earth Bag",
    "捆仙绳": "Immortal-Binding Rope",
    "==============三品法宝==============": "Grade 3 Talisman",
    "==============二品法宝==============": "Grade 2 Talisman",
    "=========生存类法宝前置=========": "Survival-type talisman prerequisite",
    "一品-乾坤袋": "Grade 1 - Heaven-Earth Bag",
    "一品-捆仙索": "Grade 1 - Immortal-Binding Cord",
    "一品-玲珑塔": "Grade 1 - Exquisite Pagoda",
    "一品-白玉瓶": "Grade 1 - White Jade Vase",
    "一品-紫金葫芦": "Grade 1 - Purple-Gold Gourd",

    # === RecipeDefs/RI_Recipes_InstallBionic.xml ===
    "安装翠玉系列": "Install jade series",
    "安装庚钢系列": "Install geng-steel series",
    "===============================五行内脏===============================": "Five Elements Organs",
    "千壶焱心": "Thousand-Cauldron Fire Heart",
    "戍土鼎胃": "Earth-Warden Cauldron Stomach",
    "肃金御肺": "Metal-Master Imperial Lungs",
    "寒灵水肾": "Cold-Spirit Water Kidneys",
    "棠木枝肝": "Crabapple Branch Liver",

    # === RecipeDefs/RI_Recipes_Armor.xml ===
    "==================================一品盔甲==================================": "Grade 1 Armor",
    "烛龙吞火盔【一品】": "Candle Dragon Fire-Devouring Helmet [Grade 1]",
    "相柳暗毒盔【一品】": "Xiangliu Poison Helmet [Grade 1]",
    "相柳白峭甲【一品】": "Xiangliu White Armor [Grade 1]",

    # === RecipeDefs/RI_Recipes_Weapon.xml ===
    "==================================二品近战==================================": "Grade 2 Melee",
    "青玉锤【二品】": "Nephrite Jade Hammer [Grade 2]",
    "巨门斧【二品】": "Jumen Axe [Grade 2]",
    "雷王枪【二品】": "Thunder Lord Lance [Grade 2]",
    "风魔刀【二品】": "Wind Demon Blade [Grade 2]",
    "==================================二品远程==================================": "Grade 2 Ranged",
    "龙头炮【二品】": "Dragon Cannon [Grade 2]",
    "飞蝇雷【二品】": "Fly Grenade [Grade 2]",
    "鬼火连弩【二品】": "Ghost Fire Crossbow [Grade 2]",
    "铁乌鸡【二品】": "Iron Throwing Ball [Grade 2]",
    "鼠须剑【二品】": "Rat Whisker Sword [Grade 2]",
    "毒心飞梭【二品】": "Poison Heart Flying Shuttle [Grade 2]",
    "古修枪": "Ancient Cultivator Rifle",
    "蚩尤怒炎戟【一品】": "ChiYou Flame Halberd [Grade 1]",
    "盘龙通天棍【一品】": "Dragon-Coiling Heaven-Staff [Grade 1]",
    "琉璃珍珠伞【一品】": "Glass Pearl Umbrella [Grade 1]",
    "破军剑【一品】": "Pojun Sword [Grade 1]",
    "斩仙剑【一品】": "Immortal-Slaying Sword [Grade 1]",
    "雷霆连珠铳【一品】": "Thunder Minigun [Grade 1]",
    "白猿长弓【一品】": "White Ape Bow [Grade 1]",

    # === ThingDefs_Races/RI_Races_Puppet.xml ===
    "====================木制傀儡===================": "Wooden Golem",
    "====================石制傀儡===================": "Stone Golem",
    "====================铁制傀儡===================": "Steel Golem",
    "================古修傀儡================": "Ancient Cultivator Golem",
    "出现在古修遗迹的傀儡，无法被玩家制作": "Golems appearing in ancient ruins; cannot be crafted by players",

    # === ThingDefs_Buildings/RI_Buildings_Puppet.xml ===
    "损坏的进程，不用管": "Damage progress — ignore",
    "前置是爆炸陷阱的前置": "Prerequisite is the explosion trap prerequisite",
    "这个最好别改，因为透明建筑的生成是按爆炸格子来计算的": "Best not to change — transparent building generation is calculated by explosion grid",
    "熄灭的爆炸类型，防止爆炸伤害傀儡，想改也可以": "Extinguish explosion type — prevents explosion damage to golems; can be changed",
    '必须要的Props，让陷阱在解锁某科技之后可主动激活，如果想改成其他科技就用对应科技的defname替换\u201cElectricity\u201d就可以': 'Required Props for trap to activate after unlocking tech; replace "Electricity" with the desired tech\'s defname',
    "需要0.00001天孵化": "Requires 0.00001 days to hatch",
    "只需要一个pawn且不希望被其他mod影响数量（有一些mod会擅自修改pawn的combatPower，说的就是你！Yayo ComBat！）用上面的方法，需要一次性生成多个pawn用下面的方法": "Only need one pawn and don't want other mods affecting the count (some mods modify pawn combatPower — looking at you, Yayo Combat!); use the above method; to spawn multiple pawns at once use the method below",
    "木制傀儡激活": "Wooden Golem Activation",

    # === SoundDefs/RI_Sound.xml ===
    "激光": "Laser",
    "苍血竹武器声": "Azure-Blood Bamboo Weapon Sound",
    "激光炮台枪声A": "Laser Turret Gunshot A",
    "激光炮台枪声B": "Laser Turret Gunshot B",

    # === WorkGiverDefs/WorkGivers.xml ===
    "制作符箓": "Craft Charm Scroll",
    "制作法宝": "Craft Talisman",

    # === ThingDefs_Items/RI_Items_Relic.xml ===
    "法门书盲盒": "Cultivation Method Book Blind Box",
    "书": "Books",
    "保底": "Guaranteed",
    "垃圾": "Junk",
    "功法书盲盒": "Skill Book Blind Box",
    "武器盲盒": "Weapon Blind Box",
    "兵器": "Weapons",
    "盔甲盲盒": "Armor Blind Box",
    "盔甲": "Armor",
    "储物袋盲盒": "Storage Bag Blind Box",
    "灵石啥的": "Spirit stones etc.",
    "丹药": "Pills",
    "金银": "Gold and Silver",

    # === ThingDefs_Misc/Weapons/RI_Weapon_Base.xml ===
    "炼器-兵器前置-高级锐器": "Forge weapon prerequisite — advanced sharp weapon",
    "贸易标签": "Trade Tag",
    "炼器-兵器前置-高级钝器": "Forge weapon prerequisite — advanced blunt weapon",
    "炼器-兵器前置-远程武器": "Forge weapon prerequisite — ranged weapon",
    "占位投射物": "Placeholder Projectile",

    # === ThingDefs_Items/RI_Items_Books.xml ===
    "================================== 炼器法门书 ====================================": "Forge Cultivation Method Book",
    "古修功法书": "Ancient Cultivator Technique Book",

    # === HediffDefs/RI_Hediffs_Damage.xml ===
    "刺痛": "Stabbing Pain",
    "风沙冲击": "Sand Shock",
    "捆绑": "Binding",

    # === AbilityDefs/RI_Route.xml ===
    "==========测试法门==========": "Test Cultivation Method",
    "1凝气境界——Noviciate rank测试": "Noviciate Rank 1 — test",
    "2固基境界——Foundation rank测试": "Foundation Rank 2 — test",
    "3化丹境界——Core formation rank测试": "Core Formation Rank 3 — test",
    "4结丹境界——Core coagulation rank测试": "Core Coagulation Rank 4 — test",
    "5灵丹境界——Core consummation rank测试": "Core Consummation Rank 5 — test",
    "6化神境界——Spirit constraint rank测试": "Spirit Constraint Rank 6 — test",
    "7元婴境界——Primordial spirit baby rank测试": "Primordial Spirit Baby Rank 7 — test",
    "8大成境界——Primordial spirit maturity rank测试": "Primordial Spirit Maturity Rank 8 — test",
    "9合体境界——Primordial spirit combine rank测试": "Primordial Spirit Combine Rank 9 — test",
    "炼器": "Forging",
    "====================炼器法门TalismanCreating====================": "Forging Cultivation Method (TalismanCreating)",
    "凝气境界——匠心": "Noviciate — Artisan's Heart",
    "化丹境界——修复": "Core Formation — Repair",
    "化神境界——工匠激励": "Spirit Constraint — Artisan's Inspiration",
    "元婴境界——百材分解": "Primordial Spirit Baby — Hundred Materials Decomposition",
    "大成境界——神机诞生": "Great Attainment — Divine Machinery Birth",
    "上面两种写法只要保证level和ability都有一个就行了": "Either format works as long as both level and ability are specified",
    "对应的境界等级": "Corresponding realm level",
    "结丹境界——铳铁再造": "Core Coagulation — Gun-Iron Reforge",
    "=====================内丹法门技能特效===========================": "Internal Elixir Method Skill Effects",
    "对应dll里thingClass，如果改了Dll这个也要改": "Corresponds to thingClass in the DLL; must change if the DLL changes",
    "对应dll里thingClass ，如果改了Dll这个也要改": "Corresponds to thingClass in the DLL; must change if the DLL changes",
    "对应原版里workerClass，想改也可以，没必要": "Corresponds to workerClass in vanilla; can be changed but not necessary",
    "不能放在屋顶下": "Cannot be placed under a roof",

    # === AbilityDefs/RI_Abilities_TalismanCreating.xml and RI_T_Effecters.xml ===
    "技能选中特效——炼器——修复": "Skill selection effect — Forging — Repair",
    "技能选中特效——炼器——分解": "Skill selection effect — Forging — Decompose",
    "技能选中特效——炼器——匠心": "Skill selection effect — Forging — Artisan's Heart",
    "技能选中特效——炼器——工匠激励": "Skill selection effect — Forging — Artisan's Inspiration",
    "技能选中特效——炼器——神机": "Skill selection effect — Forging — Divine Machinery",
    "技能选中特效——炼器——铳铁再造": "Skill selection effect — Forging — Gun-Iron Reforge",
    "技能释放特效——炼器——修复": "Skill trigger effect — Forging — Repair",
    "技能释放特效——炼器——铳铁": "Skill trigger effect — Forging — Gun-Iron",
    "读条特效": "Cast visual effect",
    "触发特效": "Trigger visual effect",
    "选中特效": "Selection visual effect",
    "光圈": "Halo effect",
    "蹦出周天功法几个字": "Pop-up circulation technique text",

    # === BackstoryDefs/Shuffled/*.xml ===
    "============古修者============": "Ancient Cultivator",
    "============古修者小孩儿============": "Ancient Cultivator Child",

    # === PawnKindDefs/RI_PawnKinds_AncientCultivators.xml ===
    "古修功法": "Ancient Cultivator Technique",
    "古修盔甲": "Ancient Cultivator Armor",
    "古修盔": "Ancient Cultivator Helmet",
    "古修者boss": "Ancient Cultivator Boss",
    "古修聚元鼎": "Ancient Cultivator Energy-Gathering Cauldron",
    "古修超人": "Ancient Cultivator Super Warrior",
    "古修超人(玩家版)": "Ancient Cultivator Super Warrior (player version)",
    "古修长刀": "Ancient Cultivator Longsword",
    "古修匕首": "Ancient Cultivator Dagger",
    "古修动力拳套": "Ancient Cultivator Power Gauntlets",
    "古修灵铳": "Ancient Cultivator Spirit Rifle",
    "=========================古修门=============================": "Ancient Cultivator Sect",
    "无古修": "Without ancient cultivator",
    "有古修": "With ancient cultivator",
    "耐打，记得加上功法hediff啥的": "Durable — remember to add cultivation method hediff etc.",

    # === ThingDefs_Buildings/RI_Buildings_Energy.xml ===
    "电气石发电机": "Tourmaline Generator",

    # === ThingDefs_Buildings/RI_Buildings_Security_Turrets.xml ===
    "怒蛟炮台": "Angry Dragon Turret",
    "怒蛟炮台子弹": "Angry Dragon Turret Bullet",
    "鲸吞炮台": "Leviathan Turret",
    "鲸吞炮台子弹": "Leviathan Turret Bullet",
    "鹤鸣炮台": "Crane-Song Turret",
    "鹤鸣炮台子弹": "Crane-Song Turret Bullet",
    '=============== \u201c怒蛟\u201d狙击炮 ===============': '"Angry Dragon" Sniper Cannon',
    '=============== \u201c鲸吞\u201d防卫炮 ===============': '"Leviathan" Defense Cannon',
    '=============== \u201c鹤鸣\u201d连射弩炮 ===============': '"Crane-Song" Rapid-Fire Crossbow Cannon',
    "=============== 庚钢 ====================": "Geng-steel Section",
    "=============== 石矩炮 ===============": "Stone Cube Cannon",
    "=============== 锈弩车 ===============": "Rusted Crossbow Cart",

    # === ThingDefs_Buildings ===
    "特殊建筑": "Special Building",
    "特殊效果": "Special Effect",
    "房屋部分": "Building Section",
    "法宝制作台": "Talisman Crafting Bench",
    "灵器锻炉": "Spirit Instrument Forge",
    "神魂宝器锻炉": "Soul Treasure Forge",
    "灵气研究器": "Qi Research Device",
    "工具桌": "Workbench",
    "拷贝台": "Copy Table",
    "铁砧": "Anvil",

    # === ThingDefs_Items ===
    "仙路-假体": "Immortal Path — Prosthetics",
    "仙路-法宝": "Immortal Path — Talismans",
    "====================================仙路-假体====================================": "Immortal Path — Prosthetics",
    "====================================仙路-法宝====================================": "Immortal Path — Talismans",
    "假体分类": "Prosthetic Category",
    "五行系列": "Five Elements Series",
    "五行器官": "Five Elements Organs",
    "五行内脏": "Five Elements Organs",
    "五行": "Five Elements",
    "五脏前置，买不到，只能自己做": "Five viscera prerequisite — cannot buy, must craft",
    "庚钢系列": "Geng-steel Series",
    "庚钢假体": "Geng-steel Prosthetics",
    "庚钢前置": "Geng-steel Prerequisite",
    "庚钢": "Geng-steel",
    "===============================庚钢===============================": "Geng-steel",
    "翠玉系列": "Jade (Green) Series",
    "翠玉前置": "Jade (Green) Prerequisite",
    "翠玉": "Jade (Green)",
    "===============================翠玉===============================": "Jade (Green)",
    "法宝": "Talisman",
    "修士宝匣，给很多好东西哦": "Cultivator treasure chest — lots of good stuff!",
    "罕见任务奖励": "Rare quest reward",
    "顶级资源，都是能放很久的": "Top-grade resources — all can be stored long-term",
    "顶级，柔玉，灵石": "Top-grade — soft jade, spirit stone",
    "中级，只有柔玉": "Intermediate — soft jade only",
    "中级": "Intermediate",
    "罗盘": "Compass",
    "玄妙石块（赌石？）": "Mysterious stones (gambling stone?)",
    "盲盒前置": "Blind Box Prerequisite",
    "商队tag": "Caravan tag",

    # === HediffDefs/RI_Hediffs_Talisman.xml ===
    "宝塔护盾": "Pagoda Shield",
    "护盾comp": "Shield comp",
    "最大盾容": "Maximum shield capacity",
    "是否一直绘制护盾泡泡，false则只在征召绘制，默认为false": "Whether to always draw the shield bubble; false = only when drafted (default false)",
    "消耗灵气": "Consumes Qi",
    "脱下法宝消失": "Talisman disappears when unequipped",
    "死亡后消失": "Disappears on death",
    "一段时间后消失": "Disappears after a period of time",
    "如意庇护": "Ruyi Protection",
    "毒铃庇护": "Toxic Bell Protection",
    "铜钱护体": "Copper Coin Protection",
    "珠光疗愈": "Pearl Light Healing",
    "琉璃珠光": "Glass Pearl Light",
    "邪不胜正！": "Evil cannot overcome righteousness!",
    "赐福": "Blessing",
    "这个就是吸入的贴图": "This is the absorption texture",
    "提供一个翻译Keyed:<RI_NoSeePawn>无法吸入装备者不可见的目标</RI_NoSeePawn>": "Translation key: <RI_NoSeePawn>Cannot absorb targets invisible to the equipment wearer</RI_NoSeePawn>",

    # === HediffDefs/RI_Hediffs_Bionics.xml ===
    "心": "Core/Heart",
    "胃": "Stomach",

    # === ThingDefs_Misc/RI_Apparel_*.xml ===
    "八卦衣": "Bagua Robe",
    "柔玉抹额【三品】": "Soft Jade Headband [Grade 3]",
    "武曲纯阳巾【二品】": "Wuqu Pure-Yang Cloth [Grade 2]",

    # === ThingDefs_Misc/Weapons/ ===
    "苍血竹武器前置": "Azure-Blood Bamboo Weapon Prerequisite",
    "苍血竹刀": "Azure-Blood Bamboo Knife",
    "苍血竹剑": "Azure-Blood Bamboo Sword",
    "苍血竹枪": "Azure-Blood Bamboo Spear",
    "苍血竹飞刀": "Azure-Blood Bamboo Throwing Knife",
    "势如破竹": "Overwhelming Force",
    "破阵斧鸣": "Formation-Breaking Axe-Cry",
    "斩仙剑": "Immortal-Slaying Sword",
    "斩仙": "Immortal Slayer",
    "破军剑": "Pojun Sword",
    "破军": "Pojun",
    "金光剑": "Golden Light Sword",
    "盘龙棍": "Dragon-Coiling Staff",
    "蚩尤戟": "ChiYou Halberd",
    "蚩尤神力": "ChiYou Divine Strength",
    "珍珠伞": "Pearl Umbrella",
    "鎏金三尖两刃刀": "Gilt Triple-Blade Knife",
    "鎏金八棱锤": "Gilt Octagonal Hammer",
    "鎏金天王甲": "Gilt Heavenly King Armor",
    "鎏金天王盔": "Gilt Heavenly King Helmet",
    "鎏金天王盔（面甲）": "Gilt Heavenly King Helmet (Faceplate)",
    "鎏金蛇矛": "Gilt Serpent Spear",
    "鎏金鱼尾斧": "Gilt Fish-Tail Axe",
    "鎏金龙虎剑": "Gilt Dragon-Tiger Sword",
    "开山斧": "Mountain-Cleaving Axe",
    "龙岩锤": "Dragon Rock Hammer",
    "霜弓": "Frost Bow",
    "飞蝗弓": "Locust Bow",
    "鹰眼火铳": "Eagle-Eye Fire Rifle",
    "短铳": "Short Rifle",
    "脱手镖": "Throwing Dart",
    "三品玄剑": "Grade 3 Mystic Sword",
    "三品追风刀": "Grade 3 Wind-Chasing Blade",
    "青囊妙药": "Herb Pouch Medicine",
    "穿心矛": "Heart-Piercing Spear",
    "龙鸣急速": "Dragon-Roar Rapid Speed",
    "速之牙": "Speed Fang",
    "拳击手套": "Boxing Gloves",
    "拳刺": "Punch Spike",
    "雷王枪": "Thunder Lord Lance",
    "龙头炮": "Dragon Cannon",
    "飞蝇雷": "Fly Grenade",
    "鬼火连弩": "Ghost Fire Crossbow",
    "铁乌鸡": "Iron Throwing Ball",
    "鼠须剑": "Rat Whisker Sword",
    "毒心梭": "Poison Heart Shuttle",
    "毒心飞梭【二品】": "Poison Heart Flying Shuttle [Grade 2]",
    "青玉锤": "Nephrite Jade Hammer",
    "巨门斧": "Jumen Axe",
    "风魔刀": "Wind Demon Blade",
    "灵铳子弹": "Spirit Rifle Bullet",
    "天兵风格武器，新增的": "Celestial soldier style weapons — newly added",
    "爆裂光束": "Burst Beam",
    "象牙项链": "Ivory Necklace",
    "铜钱吊坠": "Copper Coin Pendant",
    "檀木令牌": "Sandalwood Token",
    "令牌熏香": "Token Incense",
    "鼠须疗愈": "Rat Whisker Healing",
    "白玉露": "White Jade Dew",

    # === Effects / Visual ===
    "雷电主干": "Thunder Lightning Trunk",
    "雷电主干_差分1": "Thunder Lightning Trunk Variant 1",
    "雷电主干_差分2": "Thunder Lightning Trunk Variant 2",
    "雷电命中点": "Thunder Lightning Hit Point",
    "雷电短": "Short Thunder Lightning",
    "雷电短_差分1": "Short Thunder Lightning Variant 1",
    "雷霆机枪": "Thunder Machine Gun",
    "雷霆激发": "Thunder Activation",
    "================================持续闪电================================": "Continuous Lightning",
    "白色拖尾": "White Trail",
    "白霜灵视": "White Frost Spirit Vision",
    "白霜雨": "White Frost Rain",
    "飞沙走石": "Flying Sand and Rolling Stones",
    "破盾fleck": "Shield-Break Fleck",
    "破盾音效": "Shield-Break Sound",
    "受击fleck": "Hit Fleck",
    "受击音效": "Hit Sound Effect",
    "====势如破竹  需使用RI_Starch.RI_FLecks.RI_FleckMaker.ThrowRotationFleck====": '"Overwhelming Force" — use RI_Starch.RI_FLecks.RI_FleckMaker.ThrowRotationFleck',
    "====破阵斧鸣  需使用RI_Starch.RI_FLecks.RI_FleckMaker.ThrowRotationFleck====": '"Formation-Breaking Axe-Cry" — use RI_Starch.RI_FLecks.RI_FleckMaker.ThrowRotationFleck',

    # === General/misc ===
    "武器": "Weapon",
    "武器攻击效果": "Weapon attack effect",
    "武器特效——古修枪": "Weapon effect — ancient cultivator rifle",
    "喷火伤害": "Flamethrower damage",
    "喷火技能": "Flamethrower skill",
    "原料": "Raw Materials",
    "成本": "Cost",
    "构件": "Components",
    "组件": "Components",
    "标签": "Tag",
    "材质随机旋转": "Material random rotation",
    "气密性": "Airtightness",
    "子弹消耗": "Ammunition consumption",
    "额外的tag，给剑狂用": "Extra tag for sword fanatics",
    "生成产物": "Generated product",
    "地图": "Map",
    "垃圾很少": "Very little junk",
    "和发型同时显示": "Displayed simultaneously with hairstyle",
    "二品 近战锐器兵器 前置": "Grade 2 melee sharp weapon prerequisite",
    "二品 远程兵器 前置": "Grade 2 ranged weapon prerequisite",
    "古修盔": "Ancient Cultivator Helmet",
    "百炼铁衣": "Hundred-Forged Iron Armor",
    "烛龙甲": "Candle Dragon Armor",
    "烛龙盔": "Candle Dragon Helmet",
    "相柳甲": "Xiangliu Armor",
    "相柳盔": "Xiangliu Helmet",
    "精铁虎卫甲": "Refined Iron Tiger Guard Armor",
    "精铁虎卫盔": "Refined Iron Tiger Guard Helmet",
    "鼠眼": "Rat Eye",
    "避火": "Fire Immunity",
    "新的Flyer实体，对应dll里Verb的jumpFlyerDef": "New Flyer entity — corresponds to jumpFlyerDef in Verb in the DLL",
    "与子偕作": "Working Together",
    "炼器法门的buff": "Forging cultivation method buff",
    "30Kg偏移值": "30 kg offset value",
    "3Kg偏移值": "3 kg offset value",
    "500Kg偏移值": "500 kg offset value",
    "鎏金系列": "Gilt gold series",  # already in faction
}


# COMMENT_INNER_REPLACEMENTS: applied inside large (>200 char) comment blocks
# as substring replacements to neutralize Chinese within commented-out code
COMMENT_INNER_REPLACEMENTS = [
    ("木制傀儡激活", "Wooden Golem Activation"),
    ("电气石发电机", "Tourmaline Generator"),
    # PAWN template
    ("他/她的", "his/her"),
    ("他/她", "he/she"),
    ("宾格？", "obj?"),
]


INLINE_REPLACEMENTS = [
    # AbilityDefs/RI_Route.xml
    ("<label>炼器法门</label>",
     "<label>Forging Cultivation Method</label>"),

    # AbilityDefs/RI_Abilities_Weapon.xml
    ("<label>青玉摧破</label>",
     "<label>Nephrite Jade Shatter</label>"),

    # AbilityDefs/Ability_GlassPearlUmbrella.xml
    ("<label>琉璃珠</label>",
     "<label>Glass Pearl</label>"),

    # HediffDefs/RI_Hediffs_Talisman.xml
    ("<gizmoLabel>铜钱护体</gizmoLabel>",
     "<gizmoLabel>Copper Coin Protection</gizmoLabel>"),
    ("<gizmoTip>灵气护盾容量</gizmoTip>",
     "<gizmoTip>Qi shield capacity</gizmoTip>"),

    # ThingDef_DEV/RI_DEV_fleck.xml
    ("<label>仙路特效测试器</label>",
     "<label>Immortal Path Effects Tester</label>"),

    # ThingDefs_Buildings/Buildings_ImPower.xml
    ("<label>阵基</label>",
     "<label>Array Base</label>"),

    # ThingDefs_Buildings/RI_Buildings_Energy.xml
    ("<label>电气石发电机</label>",
     "<label>Tourmaline Generator</label>"),

    # ThingDefs_Buildings/RI_Buildings_Puppet.xml
    ("<label>木制傀儡激活</label>",
     "<label>Wooden Golem Activation</label>"),
    ("<description>木制傀儡激活</description>",
     "<description>Wooden Golem Activation</description>"),

    # ThingDefs_Buildings/RI_Buildings_Ruins.xml
    ("<label>灵气逸散的建筑</label>",
     "<label>Qi-Radiating Building</label>"),
    ("<description>建筑中蕴含有极其深厚的灵气，不断向外逸散</description>",
     "<description>The building contains extremely rich Qi that continuously radiates outward.</description>"),

    # ThingDefs_Items/RI_Items_Talisman.xml
    ("<label>聚石</label>",
     "<label>Stone-Gathering</label>"),
    ("<deathMessage>{0}被击碎了.</deathMessage>",
     "<deathMessage>{0} was shattered.</deathMessage>"),
    ("<label>狂风</label>",
     "<label>Raging Wind</label>"),
    ("<deathMessage>{0}被撕裂了.</deathMessage>",
     "<deathMessage>{0} was torn apart.</deathMessage>"),
    ("<countdownLabel>消散于</countdownLabel>",
     "<countdownLabel>Dissipates in</countdownLabel>"),

    # ThingDefs_Misc/Weapons/ — maneuver labels and charge nouns
    ("<label>棍击</label>", "<label>Staff Strike</label>"),
    ("<label>刺伤</label>", "<label>Stab</label>"),
    ("<label>枪托</label>", "<label>Gun Stock</label>"),
    ("<label>戟刃</label>", "<label>Halberd Blade</label>"),
    ("<label>戟尖</label>", "<label>Halberd Tip</label>"),
    ("<chargeNoun>蚩尤怒炎</chargeNoun>", "<chargeNoun>ChiYou Flame Charge</chargeNoun>"),
    ("<label>剑刃</label>", "<label>Sword Edge</label>"),
    ("<label>剑尖</label>", "<label>Sword Tip</label>"),
    ("<chargeNoun>破军飞剑</chargeNoun>", "<chargeNoun>Pojun Flying Sword</chargeNoun>"),
    ("<chargeNoun>诛仙斩</chargeNoun>", "<chargeNoun>Immortal-Slaying Strike</chargeNoun>"),
    ("<label>棍箍</label>", "<label>Staff Hoop Strike</label>"),
    ("<chargeNoun>千钧断岳</chargeNoun>", "<chargeNoun>Thousand-Jun Mountain-Breaker</chargeNoun>"),
    ("<label>伞柄</label>", "<label>Umbrella Handle Strike</label>"),
    ("<label>伞面</label>", "<label>Umbrella Surface Strike</label>"),
    ("<chargeNoun>琉璃珠光术</chargeNoun>", "<chargeNoun>Glass Pearl Light Art</chargeNoun>"),
    ("<label>枪管</label>", "<label>Barrel Strike</label>"),
    ("<label>斧刃</label>", "<label>Axe Blade</label>"),
    ("<chargeNoun>破阵斧鸣</chargeNoun>", "<chargeNoun>Formation-Breaking Axe-Cry</chargeNoun>"),
    ("<chargeNoun>剧毒飞刃</chargeNoun>", "<chargeNoun>Deadly Poison Flying Blade</chargeNoun>"),
    ("<label>摧破</label>", "<label>Shattering Strike</label>"),
    ("<chargeNoun>青玉摧破</chargeNoun>", "<chargeNoun>Nephrite Jade Shattering</chargeNoun>"),
    ("<label>刀刃</label>", "<label>Blade Strike</label>"),
    ("<label>刀背</label>", "<label>Blade-Back Strike</label>"),
    ("<chargeNoun>地煞狂风</chargeNoun>", "<chargeNoun>Earth Demon Storm</chargeNoun>"),
    ("<label>枪头</label>", "<label>Spearhead Strike</label>"),
    ("<label>枪杆</label>", "<label>Shaft Strike</label>"),
    ("<chargeNoun>卿云迅雷</chargeNoun>", "<chargeNoun>Swift Thunder</chargeNoun>"),
    ("<chargeNoun>势如破竹</chargeNoun>", "<chargeNoun>Overwhelming Force</chargeNoun>"),
    ("<label>炮管</label>", "<label>Cannon Barrel Strike</label>"),
    ("<chargeNoun>龙炎爆破</chargeNoun>", "<chargeNoun>Dragon Flame Blast</chargeNoun>"),
    ("<label>飞蝇雷</label>", "<label>Fly Grenade</label>"),
    ("<chargeNoun>烟雾弹</chargeNoun>", "<chargeNoun>Smoke Bomb</chargeNoun>"),
    ("<label>弩臂</label>", "<label>Crossbow Arm Strike</label>"),
    ("<chargeNoun>连射</chargeNoun>", "<chargeNoun>Rapid Fire</chargeNoun>"),
]

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')


def translate_comment(m):
    inner = m.group(1)
    if inner in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[inner]}-->"
    stripped = inner.strip()
    if stripped in TRANSLATIONS:
        return f"<!--{TRANSLATIONS[stripped]}-->"
    # For large comment blocks with Chinese, apply inner sub-replacements
    if len(inner) > 200 and CHINESE_RE.search(inner):
        result = inner
        for old, new in COMMENT_INNER_REPLACEMENTS:
            result = result.replace(old, new)
        if not CHINESE_RE.search(result):
            return f"<!--{result}-->"
        safe = stripped[:80].encode("ascii", "replace").decode("ascii")
        print(f"  UNTRANSLATED long block: <!--{safe}...-->")
        return m.group(0)
    if CHINESE_RE.search(inner):
        safe = inner.encode("ascii", "replace").decode("ascii")
        print(f"  UNTRANSLATED comment: <!--{safe}-->")
    return m.group(0)


COMMENT_RE = re.compile(r'<!--(.*?)-->', re.DOTALL)


def process_file(path):
    with open(path, encoding="utf-8") as f:
        original = f.read()
    result = COMMENT_RE.sub(translate_comment, original)
    for old, new in INLINE_REPLACEMENTS:
        result = result.replace(old, new)
    if result != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main():
    defs_root = os.path.join(REPO, "Forge", "1.6", "Defs")
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
