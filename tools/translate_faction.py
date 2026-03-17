#!/usr/bin/env python3
"""
translate_faction.py
Replaces Chinese XML comments and inline text in Faction/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_faction.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATIONS = {
    # === FactionDefs/RI_Faction_JusticeSect.xml / RI_Faction_EvilSect.xml ===
    "\u5934\u8854\u70b9\u6570\u2014\u2014\u8d21\u732e\u70b9": "Title point cost — Contribution points",
    "\u547d\u540d": "Naming",
    "\u6587\u5316": "Culture",
    "\u98ce\u683c": "Style",
    "\u5f02\u79cd": "Xenotype",
    "\u80cc\u666f\u6545\u4e8b": "Backstory",
    "\u670d\u9970": "Apparel",
    "\u6e29\u5ea6": "Temperature",
    "\u5934\u8854": "Title",
    "\u5546\u961f": "Trade caravan",
    "\u88ad\u51fb": "Raid",
    "\u7a7a\u6295\uff0c\u8d34\u56fe\u8bb0\u5f97\u6539\uff0c\u53ef\u4ee5\u662fGraphic_Random": "Drop pod — remember to change texture, can use Graphic_Random",
    "\u8bb0\u5f97\u4fee\u6539\u8d34\u56fe": "Remember to change texture",

    # === HediffDefs/RI_Hediffs_Drug.xml ===
    "\u836f\u5242\u6548\u679c": "Elixir effects",
    "<postFactor>\u4e58\u7b97\n\t\t<offset>\u52a0\u7b97": "multiply\n\t\t<offset>add",
    "60000tick=24\u5c0f\u65f6": "60000 ticks = 24 hours",
    "==================================\u4e8c\u54c1==================================": "================================== Grade 2 ==================================",
    "\u9e92\u9e9f\u590d\u5143\u4e38\u6548\u679c": "QiLin restoration pill effect",
    "15\u5929": "15 days",
    "==================================\u4e00\u54c1==================================": "================================== Grade 1 ==================================",
    "\u5403\u4e86\u5fd8\u9b42\u4e39\u4e4b\u540e\u7684\u6548\u679c\u2014\u2014\u5220\u9664\u6cd5\u95e8\uff01": "Effect of taking Oblivion Soul-Purging Elixir \u2014 delete cultivation method!",
    "\u9690\u85cf hediff": "Hidden hediff",
    "\u9690\u85cfhediff": "Hidden hediff",
    "\u5fc5\u987b\uff0c\u8fd9\u4e2a\u529f\u80fd\u662fhediff\u6d88\u5931\u65f6\u89e6\u53d1\u7684": "Required \u2014 this function triggers when the hediff disappears",
    "\u5224\u65ad\u662f\u4e0d\u662f\u8f6c\u804c\uff0c\u4e3atrue\u5c31\u662f\u4fdd\u7559\u539f\u6765\u7684\u4fee\u4e3a\uff0c\u4e0b\u9762\u7684level\u5c06\u4e0d\u751f\u6548\uff0c\u53ef\u4ee5\u5220\u6389": "Determines if this is a class transfer; if true, the original cultivation is preserved and the level setting below will not take effect and can be deleted",
    "\u4fee\u6539\u5176\u5883\u754c\uff0c\u5982\u679cIsTransfer\u662ftrue\uff0c\u90a3\u8fd9\u4e2a\u8bbe\u7f6e\u5c31\u4e0d\u9700\u8981\u4e86": "Modify its realm; if IsTransfer is true, this setting is not needed",
    "\u662f\u5426\u8fdb\u884c\u6cd5\u95e8\u64cd\u4f5c\uff0c\u5b9e\u73b0\u8f6c\u804c\u7684\u5fc5\u8981\u8bbe\u7f6e": "Whether to perform a cultivation method operation \u2014 required setting for class transfer",
    "\u9ed8\u8ba4\u4e3atrue\uff0c\u586btrue\u5c31\u662f\u9057\u5fd8\u5f53\u524d\u6cd5\u95e8\u800c\u4e0d\u6dfb\u52a0\u65b0\u6cd5\u95e8": "Default is true; set false to forget the current method without adding a new one",
    "\u6dfb\u52a0\u6cd5\u95e8\u7684\u79cd\u7c7b\uff0c\u5199route\u7684defname": "Type of cultivation method to add \u2014 write the route defname",
    "\u73b2\u73d1\u6708\u8f89\u4e39\u6548\u679c": "LingLong moonlight elixir effect",
    "\u73b2\u73d1\u75bc\u6108": "LingLong regeneration",

    # === MemeDefs/RI_Memes_Primacy.xml ===
    " \u5f71\u54cd\uff1a\u4f4e ": " Impact: Low ",
    "\u5f71\u54cd\uff1a\u4f4e": "Impact: Low",
    "\u6b63\u9053\u4e4b\u9014": "Righteous path",
    "\u4e0d\u76f8\u5bb9": "Incompatible",
    "=====规定戒律=====": "===== Specified precepts =====",
    "\u98ce\u683c": "Style",
    "\u8ba4\u540c\u7279\u6027": "Approved traits",
    "\u4e0d\u8ba4\u540c\u7279\u6027": "Disapproved traits",
    "\u90aa\u9b54\u5916\u9053": "Thran deviant path",
    " \u5f71\u54cd\uff1a\u4e2d ": " Impact: Medium ",
    "\u5f71\u54cd\uff1a\u4e2d": "Impact: Medium",
    "\u4fee\u70bc\u81f3\u4e0a": "Cultivation Supremacy",
    "\u4e4b\u540e\u66f4\u65b0\u518d\u8bf4\u5427": "Update in a future version",

    # === MemeDefs/RI_Memes_Structures.xml ===
    "\u7075\u70b3\u4fe1\u4ef0": "Spiritual Brilliance Faith",
    "\u89e3\u9501\u72ec\u6709\u5efa\u7b51": "Unlock unique buildings",

    # === FactionDefs/RulePack.xml ===
    "=============================== \u6b63\u9053 \u6d3e\u7cfb\u540d\u5b57 ===============================": "=============================== Righteous faction name ===============================",
    "=============================== \u5916\u9053 \u6d3e\u7cfb\u540d\u5b57 ===============================": "=============================== Heterodox faction name ===============================",
    "=============================== \u6d3e\u7cfb\u57fa\u5730\u540d\u5b57 ===============================": "=============================== Faction base name ===============================",

    # === RoyalTitleDef/RoyalTitlePermitDef.xml ===
    "============================= \u5934\u8854\u7684\u80fd\u529b \u524d\u7f6e =============================": "============================= Title ability prerequisite =============================",
    "============================= \u6b63\u9053\u5b97\u95e8 =============================": "============================= Righteous Sect =============================",
    "\u5916\u95e8\u5f1f\u5b50\u8bb8\u53ef": "Outer Disciple permit",
    "\u7533\u8bf7\u5efa\u6750": "Request building materials",
    "\u7533\u8bf7\u4fee\u70bc\u8d44\u6e90": "Request cultivation resources",
    "\u5185\u95e8\u5f1f\u5b50\u8bb8\u53ef": "Inner Disciple permit",
    "\u7533\u8bf7\u836f\u6750": "Request medicinal herbs",
    "\u7533\u8bf7\u4e39\u836f": "Request pills",
    "\u547c\u53eb\u4ed9\u821f": "Call Immortal Boat",
    "\u4eb2\u4f20\u5f1f\u5b50\u8bb8\u53ef": "Direct Disciple permit",
    "\u547c\u53eb\u5f1f\u5b50\u52a9\u9635": "Call disciples' assistance",
    "\u547c\u53eb\u5b97\u95e8\u8f68\u9053\u8f70\u70b8": "Call sect's orbital bombardment",
    "\u6742\u5f79\u6d3e\u9063": "Follower dispatch",
    "\u8bb0\u5f97\u4fee\u6539pawnkind": "Remember to change pawnkind",
    "记得修改pawnkind，最好是有百粮丸啥的starthediff，不用吃饭": "Remember to change pawnkind; ideally one with a starthediff like the Hundred-Grain Pill so they don't need food",

    # === RoyalTitleDef/RoyalTitleDef.xml ===
    "\u5934\u8854Base": "Title Base",
    "\u6742\u5f79": "Laborer/Servant",
    "\u5916\u95e8\u5f1f\u5b50": "Outer Disciple",
    "\u5185\u95e8\u5f1f\u5b50": "Inner Disciple",
    "\u4eb2\u4f20\u5f1f\u5b50": "Direct Disciple",
    "\u957f\u8001": "Elder",
    "\u638c\u95e8": "Sect Master",

    # === ResearchProjectDefs/RI_ResearchProjects.xml ===
    "=============================== \u5b97\u95e8\u79d1\u6280 ===================================": "=============================== Sect technology ===================================",
    "\u5b97\u95e8\u7684\u79d1\u6280\u90fd\u5728\u7075\u6c14\u9769\u547d\u4e4b\u540e": "All sect technologies come after the Qi revolution",
    "\u7535\u6c14\u77f3\u79d1\u6280": "Tourmaline technology",
    "\u7075\u6c14\u6280\u672f\u7206\u70b8": "Qi technology explosion",
    "\u5b97\u95e8\u79d1\u6280\u2014\u2014\u9700\u8981\u84dd\u56fe\u89e3\u9501\uff0c\u5148\u4e0d\u505a": "Sect technology \u2014 requires blueprint to unlock, not implemented yet",

    # === ThingDefs_Items/RI_Items_Books.xml ===
    "================================== \u65b0\u589e\u7684\u4fee\u70bc\u529f\u6cd5 ====================================": "================================== Newly added cultivation techniques ====================================",
    "\u50a8\u5b58": "Storage",
    "\u6d41\u4e91\u6b65\u6cd5": "Air step footwork",
    "\u541e\u5c71\u9b54\u529f": "Mountain-eating cultivation method",
    "玄天诀": "Mystic cultivation method",
    "\u5de7\u5de5\u901f\u4fee\u6cd5": "Refinement workspeed method",
    "\u5927\u606f\u9f9f\u7720\u529f": "Tortoise meditation method",

    # === ThingDefs_Items/RI_Items_Books_Evil.xml ===
    "================================== \u90aa\u4fee\u529f\u6cd5 ====================================": "================================== Evil cultivation techniques ====================================",
    "\u641c\u9b42\u672f": "Soul searching technique",

    # === ThingDefs_Items/RI_Items_NewDrugs.xml ===
    "==========================\u3010\u4e00\u54c1\u3011\u6e6e\u5c18\u5fd8\u9b42\u4e39==========================": "========================== [Grade 1] Oblivion Soul-Purging Elixir ==========================",
    "==========================\u3010\u4e00\u54c1\u3011\u73b2\u73d1\u6708\u8f89\u4e39==========================": "========================== [Grade 1] Exquisite Moonlight Elixir ==========================",
    "\u4e00\u54c1\u836f \u73b2\u73d1\u4ed9\u917f": "Grade 1 elixir \u2014 Exquisite Immortal Brew",
    "\u4e00\u54c1\u836f \u73ca\u745a\u917f": "Grade 1 elixir \u2014 Coral Brew",
    "\u4e00\u54c1\u836f \u73b2\u73d1\u6708\u8f89\u4e39": "Grade 1 pill \u2014 Exquisite Moonlight Pill",
    "=================\u4e8c\u54c1\u4e39\u836f\u2014\u2014\u9e92\u9e9f\u4e38=================": "================= Grade 2 pill \u2014 QiLin Pill =================",
    "\u6d53\u7f29\u7075\u6db2": "Condensed spiritual liquid",

    # === TraderKindDef/RI_JusticeSect_TraderGeneral.xml ===
    "=================\u6b63\u9053\u95e8\u6d3e\u7684\u5546\u961f=================": "================= Righteous sect caravan =================",
    "\u4e4b\u540e\u52a0\u5165\u548c\u56db\u8c61\u7b49\u62d3\u5c55\u7684\u8054\u52a8": "Will add integration with SiXiang and other expansions later",
    "\u4fee\u884c\u5f1f\u5b50": "Cultivating disciple",
    "========\u51fa\u552e========": "======== For sale ========",
    "========\u8d2d\u4e70========": "======== For purchase ========",
    "\u5343\u6750\u5e9c\u2014\u2014\u4e13\u95e8\u5356\u5404\u79cd\u5efa\u6750\uff0c\u539f\u6599\uff0c\u4e0d\u5356\u4fee\u70bc\u7269\u8d44": "Qian Cai Fu \u2014 sells various building materials and raw materials, not cultivation supplies",
    "\u96f6\u90e8\u4ef6": "Components",
    "\u76ae\u6599": "Leather/Textiles",
    "\u836f\u54c1": "Medicine",
    "\u5e03\u5e1b\u83fd\u7cdf\u571f\u6728": "Cloth, grain, earth, wood",
    "\u4e39\u836f": "Pills/Elixirs",
    "\u4ed9\u8def\u98df\u54c1": "Immortal path food",
    "\u9752\u971b\u5546\u2014\u2014\u5356\u4fee\u70bc\u7269\u8d44\uff0c\u4e39\u836f\uff0c\u4e4b\u7c7b\u7684\u9ad8\u7ea7\u73a9\u610f": "Qing Xiao merchant \u2014 sells cultivation supplies, pills, and high-end goods",
    " \u52a8\u7269 ": " Animals ",
    "\u52a8\u7269": "Animals",
    "\u4e07\u5377\u4e66\u884c\u2014\u2014\u53ea\u4e70\uff0c\u5356\u4e66": "Myriad Books Caravan \u2014 buy only, sell books",
    "\u6cd5\u95e8\u4e66 ": "Cultivation method books ",
    "\u6cd5\u95e8\u4e66": "Cultivation method books",
    "\u901a\u7528\u529f\u6cd5\u4e66 ": "General technique books ",
    "\u901a\u7528\u529f\u6cd5\u4e66": "General technique books",
    "\u4fee\u70bc\u529f\u6cd5\u4e66 ": "Cultivation technique books ",
    "\u4fee\u70bc\u529f\u6cd5\u4e66": "Cultivation technique books",
    "\u5b97\u95e8\u4e66\u5377 ": "Sect scroll books ",
    "\u5b97\u95e8\u4e66\u5377": "Sect scroll books",
    "\u6b62\u6208\u9986": "Peacekeeper armory",
    "\u57fa\u7840\u539f\u6599 ": "Basic materials ",
    "\u57fa\u7840\u539f\u6599": "Basic materials",
    "\u539f\u7248\u6b66\u5668 ": "Vanilla weapons ",
    "\u539f\u7248\u6b66\u5668": "Vanilla weapons",
    "\u539f\u7248\u76d4\u7532 ": "Vanilla armor ",
    "\u539f\u7248\u76d4\u7532": "Vanilla armor",
    "\u4ed9\u8def\u6b66\u5668 ": "Immortal path weapon ",
    "\u4ed9\u8def\u6b66\u5668": "Immortal path weapon",
    "\u4ed9\u8def\u76d4\u7532 ": "Immortal path armor ",
    "\u4ed9\u8def\u76d4\u7532": "Immortal path armor",
    "\u82cd\u8840\u7af9\u7cfb\u5217": "Azure-blood bamboo series",
    "\u9570\u91d1\u7cfb\u5217": "Gilt gold series",
    "\u4e8c\u54c1": "Grade 2",
    "\u4e09\u54c1": "Grade 3",
    "\u8d21\u732e\u5de1\u6536\u961f": "Contribution patrol collector",
    "========\u5151\u6362\u8d21\u732e\u70b9\u7684\u7269\u54c1========": "======== Items for exchanging contribution points ========",
    "\u9ec4\u91d1": "Gold",
    "\u7075\u77f3": "Spirit stone",
    "\u9752\u51a5\u6811\u79cd": "QingMing tree seed",
    "\u67d4\u7389": "Soft jade",
    "\u9752\u7389\u9ad3": "Qingming marrow",
    "\u7075\u82bd": "Spirit sprout",
    "\u4e0a\u54c1\u7075\u82bd": "High-grade spirit sprout",
    "\u4e0b\u54c1\u7075\u82bd": "Low-grade spirit sprout",
    "\u9752\u7389\u4ed9\u9732": "QingMing jade dew",
    "\u6d17\u9ad3\u7389\u6db2": "Marrow-washing jade liquid",
    "\u4ed9\u8def\u7684\u5175\u5668\u76d4\u7532\uff0c\u4ec0\u4e48\u5546\u961f\u90fd\u6536": "Immortal path weapons and armor \u2014 accepted by any caravan",

    # === TraderKindDef/RI_EvilSect_TraderGeneral.xml ===
    "=================\u5916\u9053\u95e8\u6d3e\u7684\u5546\u961f=================": "================= Heterodox sect caravan =================",
    "\u6697\u574a": "Shadow market",
    "\u8d29\u5974\u4eba": "Slave trafficker",

    # === TraderKindDef/TraderKinds_Orbital_Immortals.xml ===
    "\u82cd\u7a79\u5546\u65c5 \u8f68\u9053\u8d27\u8239": "Celestial Caravan orbital cargo ship",
    "\u57fa\u7840\u6750\u6599 ": "Basic materials ",
    "\u4f20\u5355": "Pamphlet",
    "\u547c\u53eb\u5668": "Caller device",
    "\u836f\u54c1 ": "Medicine ",
    "\u4e09\u54c1\u6b66\u5668": "Grade 3 weapon",
    "\u5bfb\u5e38\u8863\u7269 ": "Ordinary clothing ",
    "\u5bfb\u5e38\u8863\u7269": "Ordinary clothing",
    "\u901a\u7528\u529f\u6cd5\u4e66 ": "General technique books ",
    "\u6545\u4e8b\u4e66 ": "Story books ",
    "\u6545\u4e8b\u4e66": "Story books",
    "\u4e70\u7684\u4e1c\u897f ": "Things to buy ",
    "\u4e70\u7684\u4e1c\u897f": "Things to buy",

    # === TraderKindDef/RI_TraderKinds_Base_JusticeSect.xml ===
    "\u6b63\u9053\u6d3e\u7cfb\u5b9a\u5c45\u70b9\u5356\u7684\u4e1c\u897f": "Items sold at righteous faction settlements",
    "\u57fa\u7840\u7269\u8d44": "Basic supplies",
    "\u86a9\u5375": "Silkworm eggs",
    "\u6536\u8d2d ": "Purchasing ",
    "\u6536\u8d2d": "Purchasing",
    "\u4ed9\u8def\u6b66\u5668 ": "Immortal path weapon ",
    "\u4ed9\u8def\u76d4\u7532 ": "Immortal path armor ",

    # === HediffDefs/Hediff2.xml ===
    "\u805a\u6c14\u51a5\u60f3\u6cd5": "Focused qi meditation method",
    "\u51a5\u60f3\u6307\u70b9": "Meditation guidance",

    # === HediffDefs/RI_Hediffs_CultivationMethod.xml ===
    "\u5927\u606f\u9f9f\u7720\u529f \u9f9f\u7720\u4e4b\u6cd5": "Tortoise meditation method \u2014 Tortoise sleep technique",
    "\u541e\u5c71\u9b54\u529f \u541e\u5c71\u9b54\u529f": "Mountain-eating cultivation method",
    "玄天诀 玄天秘法": "Mystic cultivation method — Mystic heaven secret art",
    "\u767e\u70bc\u901f\u4fee \u7cbe\u7814\u7ec6\u5de5": "Refinement workspeed method \u2014 Careful craftsmanship",
    "\u6d41\u4e91\u6b65\u6cd5 \u6d41\u4e91\u6b65\u6cd5": "Air step footwork method",

    # === HediffDefs/RI_Hediffs_Shield.xml ===
    "====================\u6563\u4fee\u4eec\u5237\u51fa\u6765\u7684\u62a4\u76fe\uff08\u524d\u7f6e\uff09====================": "==================== Shield spawned by rogue cultivators (prerequisite) ====================",

    # === ThingDefs/Things_Special.xml ===
    "\u4fee\u4ed9\u7248\u672c\u7684\u7a7f\u68ad\u673a": "Cultivation-themed shuttle",

    # === PawnKindDefs_Humanlikes/RI_PawnKinds_JusticeSect.xml ===
    "\u6b63\u9053\u5b97\u95e8pawn\u7684base": "Righteous sect pawn base",
    "\u6b63\u9053\u6d3e\u7cfb": "Righteous faction",
    "\u80cc\u666f\u6545\u4e8b": "Backstory",
    "\u7981\u6b62\u7279\u6027": "Prohibited traits",
    "\u5047\u4f53": "Prosthetic",
    "\u643a\u5e26\u7269\u8d44": "Carried supplies",
    "\u4fe8\u8679\u6297\u6027": "Captive resistance",
    "\u6218\u6597\u529b~": "Combat power ~",
    "\u5e74\u9f84": "Age",
    "\u8863\u670d": "Clothing",
    "\u6b66\u5668": "Weapon",
    "\u9644\u5e26hediff\uff08\u63a7\u5236\u5883\u754c\u548c\u5f00\u5c40\u81ea\u5e26buff\uff09": "Starting hediffs (controls realm and initial buffs)",
    "\u643a\u5e26\u98df\u7269": "Carried food",
    "\u767e\u7cae\u4e38\u6548\u679c": "Hundred-Grain Pill effect",
    "\u6742\u5f79": "Laborer/Servant",
    "\u5916\u95e8\u5f1f\u5b50": "Outer Disciple",
    "\u5185\u95e8\u5f1f\u5b50": "Inner Disciple",
    "\u4eb2\u4f20\u5f1f\u5b50": "Direct Disciple",
    "\u62a4\u6cd5 \u70bc\u4f53\u5316\u795e": "Sect guard \u2014 body tempering cultivation",
    "\u6267\u4e8b\u2014\u2014\u4e00\u822c\u53ea\u4f5c\u4e3a\u5546\u8d29\u51fa\u73b0": "Deacon \u2014 generally only appears as trader",
    "\u957f\u8001 \u5185\u4e39\u5927\u6210": "Elder \u2014 internal elixir mastery",
    "\u638c\u95e8 \u5185\u4e39\u767b\u4ed9": "Sect Master \u2014 internal elixir ascension",

    # === BackstoryDefs/Shuffled/RI_Cultivator_Child.xml ===
    "\u6240\u6709\u7ae5\u5e74\u4fee\u70bc\u8005 \u80cc\u666f\u6545\u4e8b \u524d\u7f6e": "All child cultivator backstory prerequisite",
    "\u90fd\u80fd\u5e72\u66b4\u529b\u5de5\u4f5c\u548c\u7814\u7a76": "Can all do violent work and research",
    "============\u901a\u7528\u5e7c\u5e74 \u524d\u7f6e============": "============General child backstory prerequisite============",
    "\u5947\u9047": "Adventure",
    "\u6d77\u8fb9\u7684\u5f03\u513f": "Abandoned child by the sea",
    "\u901a\u7075\u5b69\u7ae5": "Spirit-communing child",
    "\u54d1\u5df4": "Mute child",
    "============\u7279\u6b8a\u5e7c\u5e74 \u524d\u7f6e============": "============Special child backstory prerequisite============",
    "\u7389\u4ed9\u8f6c\u4e16": "Reincarnation of the Jade Immortal",
    "\u5996\u517d\u5316\u5f62": "Beast transformation",
    "\u7ea2\u5b69\u513f": "Red boy",
    "\u7761\u68a6\u7ae5\u5b50": "The dreaming child",
    "\u7a7f\u8d8a\u4e4b\u4eba": "Traverser",
    "============\u6b79\u4fee\u5e7c\u5e74 \u524d\u7f6e============": "============Evil cultivator child prerequisite============",
    "\u88ab\u593a\u820d\u7684\u5e7c\u7ae5": "Child occupied by a soul",
    "============\u5b97\u95e8\u5e7c\u5e74 \u524d\u7f6e============": "============Sect youth prerequisite============",
    "\u5b97\u95e8\u65b0\u661f": "Rising star of the sect",
    "\u5b97\u95e8\u7ea8\u7ee9\u5f1f\u5b50": "Rich sect disciple",
    "\u7c97\u9c81\u9738\u9053\u7684\u5f1f\u5b50": "Rude and dominant disciple",
    "\u8001\u5b9e\u7684\u5b97\u95e8\u5f1f\u5b50": "Honest sect disciple",
    "\u788c\u788c\u65e0\u4e3a\u7684\u5f1f\u5b50": "Mediocre disciple",

    # === BackstoryDefs/Shuffled/RI_Cultivator_Adult.xml ===
    "\u6240\u6709\u6210\u5e74\u4fee\u70bc\u8005 \u80cc\u666f\u6545\u4e8b \u524d\u7f6e": "All adult cultivator backstory prerequisite",
    "============\u6563\u4fee\u6210\u5e74 \u524d\u7f6e============": "============Rogue cultivator adult prerequisite============",
    "\u6563\u4fee\u4e39\u5e08": "Rogue cultivator alchemist",
    "\u9a47\u9065\u6563\u4fee": "Carefree independent cultivator",
    "\u5584\u826f\u6563\u4fee": "Kind free cultivator",
    "\u6d77\u4e4b\u7940\u6c11": "People of the sea",
    "\u8352\u539f\u65c5\u8005": "Wasteland traveler",
    "\u5b97\u95e8\u5e78\u5b58\u8005": "Sect survivor",
    "============\u6b79\u4fee\u6210\u5e74 \u524d\u7f6e============": "============Evil cultivator adult prerequisite============",
    "\u7075\u82bd\u5077\u730e\u8005": "Energy root poacher",
    "\u593a\u820d\u4e4b\u4eba": "Occupy the soul",
    "\u6d41\u4ea1\u90aa\u4fee": "Exiled evil cultivator",
    "\u6df1\u9677\u9b54\u9053": "Deeply consumed in evil",
    "\u9ed1\u6697\u4e4b\u4eba": "Hidden in the Darkness",
    "============\u7279\u6b8a\u6210\u5e74 \u524d\u7f6e============": "============Special adult backstory prerequisite============",
    "\u4ed9\u4eba\u6740\u624b": "Immortal Killer",
    "\u4ed9\u6843\u5927\u4ea8": "Immortal Peach Magnate",
    "\u9668\u843d\u5929\u624d": "Fallen genius",
    "\u5927\u7231\u4ed9\u5c0a": "Great-love immortal",
    "\u9152\u4e2d\u4ed9": "Immortal in wine",
    "\u8d64\u9762\u9b3c": "Red-faced demon",
    "\u655b\u5c38\u4eba": "Corpse collector",
    "============\u6b63\u9053\u95e8\u6d3e\u4fee\u58eb\u6210\u5e74 \u524d\u7f6e============": "============Righteous sect adult cultivator prerequisite============",
    "\u5065\u5eb7\u7684\u95e8\u6d3e\u4fee\u58eb": "Healthy sect cultivator",
    "\u4f18\u79c0\u7684\u95e8\u6d3e\u4fee\u58eb": "Excellent sect cultivator",
    "============\u5916\u9053\u95e8\u6d3e\u4fee\u58eb\u6210\u5e74 \u524d\u7f6e============": "============Heterodox sect adult cultivator prerequisite============",
    "\u7089\u9dbc\u7231\u597d\u8005": "Furnaces lover",

    # === RoyalTitleDef/RoyalTitleThought.xml ===
    "============================= \u5934\u8854\u6570\u91cf \u524d\u7f6e =============================": "============================= Title rank prerequisite =============================",

    # === Ability/Ability2.xml ===
    "\u805a\u6c14\u7075\u57df": "Focused Qi Domain",

    # === PawnKindDefs_Humanlikes/RI_PawnKinds_EvilSect.xml ===
    "\u5916\u9053\u5b97\u95e8pawn\u7684base": "Heterodox sect pawn base",
    "\u5916\u9053\u6d3e\u7cfb": "Heterodox faction",
    "\u4fe8\u8679\u6297\u6027": "Captive resistance",
    "\u5916\u9053\u5165\u95e8": "Heterodox beginner",
    "\u5916\u9053\u4fee\u58eb\u2014\u2014\u8d1f\u8d23\u5f53\u5546\u8d29": "Heterodox cultivator \u2014 acts as trader",
    "\u5916\u9053\u9aa8\u5e72": "Heterodox cadre",
    "\u5916\u9053\u5934\u76ee": "Heterodox leader",
    "\u6559\u4e3b": "Cult master",

    # === PawnKindDefs_Humanlikes/RI_PawnKinds_Follower.xml ===
    "\u65b0\u5b97\u95e8\u5f00\u5c40\u7684\u6742\u5f79": "Laborer for new sect start",
    "\u76ee\u524d\u8fd8\u662f\u6d4b\u8bd5\u7528\u7684\uff0c\u7279\u6b8a\u5355\u4f4d": "Currently still for testing — special unit",
    "\u91d1\u7532\u536b\u58eb": "Golden guard",

    # === ThingDefs_Items/RI_Items_NoteBook.xml ===
    "RI_ReadableBook_Base\u5728\u6838\u5fc3": "RI_ReadableBook_Base in Core",
    "\u53ea\u6709\u5b97\u95e8\u7684\u4e66\u7c4d\u5546\u961f\u624d\u5356\u8fd9\u4e2a": "Only the sect's book trader sells this",
    "\u82cd\u7a79\u5546\u65c5\u4f20\u5355": "Celestial Caravan flyer",

    # === ThingDefs_Items/RI_Items_RawPlant.xml ===
    "\u73b2\u73d1\u73cd\u679c": "LingLong precious fruit",
    "\u5403\u4e86\u73b2\u73d1\u73cd\u679c": "Ate LingLong fruit",

    # === Scenarios/Scenarios.xml ===
    "\u5f00\u5c40\u7269\u8d44 ": "Starting supplies ",
    "\u5f00\u5c40\u7269\u8d44": "Starting supplies",

    # === ResearchProjectDefs/RI_ResearchProjects.xml ===
    "\u7075\u6c14\u6280\u672f\u7206\u70b8": "Qi technology explosion",

    # === BackstoryDefs comments with pawn template block ===
    # The large template comment block is the same in both child and adult files.
    # It contains pronoun examples and skill list — treat as developer notes.
    "[PAWN_nameDef]\n\t[PAWN_pronoun]\u4ed6/\u5979\n\t[PAWN_possessive]\u4ed6/\u5979\u7684\n\t[PAWN_objective]\u5bbe\u683c\uff1f\n\t\n\t<workDisables>\n\t<li>ManualDumb</li>\n\t</workDisables>\n\t\n\t<Melee>3</Melee>\n\t<Plants>3</Plants>\n\t<Medicine>2</Medicine>\n\t<Social>-2</Social>\n\t<Construction>3</Construction>\u5efa\u9020\n\t<Animals>3</Animals>\n\t<Crafting>3</Crafting>\n\t<Mining>8</Mining>\n\t<Cooking>-4</Cooking>\n\t<Shooting>3</Shooting>\n\t<Intellectual>2</Intellectual>\n\t\n\t<requiredWorkTags>\n\t<li>Violent</li>\n\t<li>Animals</li>\n\t<li>ManualDumb</li>\n\t</requiredWorkTags>\n\t\n\t<bodyTypeMale>Male</bodyTypeMale>\n\t<bodyTypeFemale>Female</bodyTypeFemale>\n\t\n\t<possessions>\n\t<Cloth>10</Cloth>\n\t</possessions>\n\t": "Developer template — pawn pronoun and skill reference block",

    # Variant with Cooking before Mining (child file)
    "[PAWN_nameDef]\n\t[PAWN_pronoun]\u4ed6/\u5979\n\t[PAWN_possessive]\u4ed6/\u5979\u7684\n\t[PAWN_objective]\u5bbe\u683c\uff1f\n\t\n\t<workDisables>\n\t<li>ManualDumb</li>\n\t</workDisables>\n\t\n\t<Melee>3</Melee>\n\t<Plants>3</Plants>\n\t<Medicine>2</Medicine>\n\t<Social>-2</Social>\n\t<Construction>3</Construction>\u5efa\u9020\n\t<Animals>3</Animals>\n\t<Crafting>3</Crafting>\n\t<Cooking>-4</Cooking>\n\t<Mining>8</Mining>\n\t<Shooting>3</Shooting>\n\t<Intellectual>2</Intellectual>\n\t\n\t<requiredWorkTags>\n\t<li>Violent</li>\n\t<li>Animals</li>\n\t<li>ManualDumb</li>\n\t</requiredWorkTags>\n\t\n\t<bodyTypeMale>Male</bodyTypeMale>\n\t<bodyTypeFemale>Female</bodyTypeFemale>\n\t\n\t<possessions>\n\t<Cloth>10</Cloth>\n\t</possessions>\n\t": "Developer template — pawn pronoun and skill reference block",

    "\u6240\u6709\u6210\u5e74\u4fee\u70bc\u8005 \u80cc\u666f\u6545\u4e8b \u524d\u7f6e": "All adult cultivator backstory prerequisite",
    "\u90fd\u80fd\u5e72\u66b4\u529b\u5de5\u4f5c\u548c\u7814\u7a76": "Can all do violent work and research",
    "\u6240\u6709\u7ae5\u5e74\u4fee\u70bc\u8005 \u80cc\u666f\u6545\u4e8b \u524d\u7f6e": "All child cultivator backstory prerequisite",

    # === FactionDefs/RI_Faction_EvilSect.xml ===
    "leader\u5fc5\u987b\u51fa\u73b0\u5728\u88ad\u51fb\u7684group\u91cc\u9762\uff0c\u4e0d\u7136\u4f1a\u62a5\u7ea2\u5b57": "Leader must appear in the raid group list, otherwise red errors will occur",

    # === FactionDefs/RI_Faction_JusticeSect.xml / RI_Faction_EvilSect.xml ===
    " 普通修仙者袭击 ": " Normal cultivator raid ",
    "普通修仙者袭击": "Normal cultivator raid",

    # === Ability/Ability.xml — section headers per cultivation method ===
    "大息龟眠功A": "Tortoise Meditation Method A",
    "读条特效": "Cast visual effect",
    "光圈": "Halo effect",
    "触发特效": "Trigger visual effect",
    "吞山魔功B": "Mountain-eating Cultivation Method B",
    "能学会": "Can be learned",
    "玄天诀C": "Mystic Cultivation Method C",
    "巧工速修法D": "Refinement Workspeed Method D",
    "流云步法E": "Air Step Footwork E",

    # === BackstoryDefs/Shuffled/RI_Cultivator_Adult.xml ===
    "逍遥散修": "Carefree independent cultivator",
    "炉鼎爱好者": "Furnace lover",

    # === BackstoryDefs/Shuffled/RI_Cultivator_Child.xml ===
    "宗门纨绔弟子": "Rich sect disciple",

    # === HediffDefs/RI_Hediffs_Drug.xml ===
    "默认为true，填false就是遗忘当前法门而不添加新法门": "Default is true; set false to forget the current method without adding a new one",
    "浓缩灵液效果": "Condensed spiritual liquid effect",
    "玲珑疗愈": "LingLong regeneration",

    # === IdeoSymbolDefs/IdeoIconDefs_Universal.xml ===
    "文化符号，先不写具体meme，之后再补上": "Culture symbols — specific memes to be added later",
    "古修": "Ancient cultivation",
    "中国文化：一大堆": "Chinese culture: a large variety",
    "龙": "Dragon",
    "丹药：丹炉，葫芦": "Pills: alchemy furnace, gourd",
    "元素：云，天空，太阳": "Elements: clouds, sky, sun",
    "鱼": "Fish",
    "自然：花，树，草": "Nature: flowers, trees, grass",
    "掠夺：战争，头骨": "Plunder: war, skulls",
    "灵气：气，修炼": "Qi: aura, cultivation",

    # === Ideology/RitualAttachableOutcomeEffectDef.xml ===
    "发现柔玉": "Find liquid jade",
    "灵气滋养": "Qi nourishment",

    # === PreceptDefs/Precepts_Role.xml ===
    "新增两个职位": "Two new roles added",
    "太上长老": "Grand elder",
    "给予的能力": "Granted abilities",
    "首席护法": "Chief guard",
    "无法工作": "Cannot work",

    # === RecipeDefs/RI_Recipes_Books.xml ===
    "合成玄天诀": "Craft Mystic cultivation method",
    "合成商船呼叫器": "Craft Celestial Caravan orbital pager",

    # === RecipeDefs/RI_Recipes_Drugs.xml ===
    "麒麟丹": "QiLin restoration pill",
    "=============================一品丹=============================": "============================= Grade 1 pill =============================",
    "忘魂丹": "Oblivion soul-purging elixir",
    "玲珑月辉丹": "LingLong moonlight elixir",
    "炼制浓缩灵液": "Refine condensed spiritual liquid",
    "制作玲珑仙酿": "Make LingLong immortal wine",

    # === Scenarios/Scenarios.xml ===
    "装备": "Equipment",
    "开局科技": "Starting research",

    # === StyleCategoryDefs/StyleCategoryDefs.xml ===
    "仙路文化风格——无界之象": "Immortal path culture style — Boundless Form",
    "武器类": "Weapons",
    "钉头锤": "Mace",
    "短剑": "Short sword",
    "短矛": "Short spear",
    "匕首": "Dagger",
    "破墙斧": "Breach axe",
    "长剑": "Long sword",
    "长矛": "Spear",
    "家具类": "Furniture",
    "祭坛1x1": "Altar 1x1",
    "祭坛2x3": "Altar 2x3",
    "祭坛3x3": "Altar 3x3",
    "立柱": "Column",
    "落地灯": "Standing lamp",
    "火炬": "Torch",
    "凳子": "Stool",
    "餐椅": "Dining chair",
    "桌子1x2": "Table 1x2",
    "桌子2x2": "Table 2x2",
    "桌子3x3": "Table 3x3",
    "桌子2x4": "Table 2x4",
    "讲台": "Lectern",
    "后续继续添加家具，还能增加地毯一类的group": "Will continue to add furniture, can also add carpet-type groups",

    # === ThingDefs_Items/RI_Items_Unfinished.xml ===
    "苍穹商旅呼叫器": "Celestial Caravan orbital pager",
    " 允许使用 ": " Allow use ",
    "允许使用": "Allow use",
    " 指定商船 ": " Specify trade ship ",
    "指定商船": "Specify trade ship",
    " 1 天 ": " 1 day ",
    "1 天": "1 day",

    # === ThingDefs_Misc/RI_Apparel_Normal.xml ===
    "芙蓉冠": "Flonne crown",
    "贸易标签": "Trade tag",
    "莲花冠": "Lotus crown",
    "仙门斗篷": "Immortal sect cloak",
    "制式交领短衫": "Standard cross-collar shirt",

    # === ThingDefs_Plants/Plants_Cultivated_Farm.xml ===
    "=========================== 玲珑果树 ==============================": "=========================== LingLong fruit tree ==============================",

    # === ThingStyleDefs/ThingStyleDefs.xml ===
    " 原版文化的Bases，只是家具有用 ": " Vanilla culture Bases — only furniture applies ",
    "原版文化的Bases，只是家具有用": "Vanilla culture Bases — only furniture applies",
    " 仙路文化风格——无界之象 ": " Immortal path culture style — Boundless Form ",
    "家具": "Furniture",

    # === TraderKindDef/RI_JusticeSect_TraderGeneral.xml ===
    "布帛菽粟土木": "Cloth, grain, earth, wood",
    "青霄商——卖修炼物资，丹药，之类的高级玩意": "Qing Xiao merchant — sells cultivation supplies, pills, and high-end goods",
    "鎏金系列": "Gilt gold series",

    # === TraderKindDef/RI_TraderKinds_Base_JusticeSect.xml ===
    "蚕卵": "Silkworm eggs",

    # === TraderKindDef/TraderKinds_Orbital_Immortals.xml ===
    " 基础材料 ": " Basic materials ",
    "基础材料": "Basic materials",

    # === RoyalTitleDef/RoyalTitlePermitDef.xml (duplicate key fix) ===
    "============================= 异教 =============================": "============================= Heterodox Sect =============================",
    " 普通修仙者 ": " Normal cultivator ",

    # === PawnKindDefs_Humanlikes (俘虏抗性 — captive resistance) ===
    "俘虏抗性": "Captive resistance",
}


INLINE_REPLACEMENTS = [
    # RI_Meme_Culture.xml — CultureDef label / description
    ("<label>\u7075\u70b3\u4fe1\u4ef0</label>",
     "<label>Spiritual Brilliance Faith</label>"),
    ("<description>\u98d8\u98d8\u4e4e\u5982\u9057\u4e16\u72ec\u7acb\uff0c\u7fbd\u5316\u800c\u767b\u4ed9</description>",
     "<description>Drifting, isolated from the world, transforming and ascending to immortality</description>"),

    # RI_Meme_Culture.xml — RulePackDef leader title
    ("<li>r_leaderTitle->\u638c\u95e8</li>",
     "<li>r_leaderTitle->Sect Master</li>"),

    # RI_Memes_Structures.xml — generalRules
    ("<li>memeHyphenPrefix->\u9053</li>",
     "<li>memeHyphenPrefix->Dao</li>"),
    ("<li>memeLeaderNoun->\u5fc3\u9b44</li>",
     "<li>memeLeaderNoun->Soul</li>"),
    ("<li>memeLeaderNoun->\u51b3\u65ad\u8005</li>",
     "<li>memeLeaderNoun->Arbiter</li>"),
    ("<li>memeLeaderNoun->\u5b97\u4e3b</li>",
     "<li>memeLeaderNoun->Patriarch</li>"),
    ("<li>memeLeaderAdjective->\u6b63\u9053</li>",
     "<li>memeLeaderAdjective->Righteous</li>"),
    ("<li>memeLeaderAdjective->\u4ec1\u4e49</li>",
     "<li>memeLeaderAdjective->Benevolent</li>"),
    ("<li>memeLeaderAdjective->\u609f\u9053</li>",
     "<li>memeLeaderAdjective->Enlightened</li>"),
    ("<li>memeMoralist->\u8c0b\u58eb</li>",
     "<li>memeMoralist->Counselor</li>"),
    ("<li>memeMoralist->\u9053\u5b66\u5bb6</li>",
     "<li>memeMoralist->Way Scholar</li>"),
    ("<li>memeMoralist->\u5fb7\u884c\u8005</li>",
     "<li>memeMoralist->Virtuous One</li>"),
    ("<li>memeMoralist->\u4ed9\u5bb6</li>",
     "<li>memeMoralist->Immortal Sage</li>"),
    ("<li>memeMoralist->\u667a\u8005</li>",
     "<li>memeMoralist->Sage</li>"),
    ("<li>memeMoralist->\u5112\u58eb</li>",
     "<li>memeMoralist->Confucian Scholar</li>"),
    ("<li>memeMoralist->\u8fa9\u58eb</li>",
     "<li>memeMoralist->Orator</li>"),

    # RI_Memes_Primacy.xml — MemeDef description
    ("<description>\u5fc3\u5982\u660e\u955c\uff0c\u7ec8\u6210\u5927\u9053\u3002\u6211\u4eec\u59cb\u7ec8\u884c\u8d70\u4e8e\u6b63\u9053\u4e4b\u4e0a\uff0c\u4e0d\u4f1a\u504f\u79bb\u3002</description>",
     "<description>Heart clear as a mirror, achieving the supreme Way. We always walk the righteous path, never deviating.</description>"),

    # HediffDefs/RI_Hediffs_Drug.xml — inline label / description for DeleteIA
    ("<description>\u5220\u9664\u6cd5\u95e8</description>",
     "<description>Delete cultivation method</description>"),
    ("<label>\u5220\u9664\u6cd5\u95e8</label>",
     "<label>Delete cultivation method</label>"),

    # ThingDefs/Things_Special.xml — Immortal Boat labels/descriptions
    ("<label>\u4ed9\u821f</label>",
     "<label>Immortal Boat</label>"),
    ("<description>\u4ed9\u821f</description>",
     "<description>Immortal Boat</description>"),
    ("<description>\u4ed9\u821f\u884c\u4e8e\u9ad8\u7a7a</description>",
     "<description>The Immortal Boat soars at high altitude</description>"),
    ("<label>\u4ed9\u821f (incoming)</label>",
     "<label>Immortal Boat (incoming)</label>"),
    ("<label>\u4ed9\u821f (leaving)</label>",
     "<label>Immortal Boat (leaving)</label>"),

    # FactionDefs/RI_Faction_JusticeSect.xml — drop pod ThingDef label
    ("<label>\u4ed9\u821f\uff1a\u98de\u884c\u4e2d</label>",
     "<label>Immortal Boat: in flight</label>"),

    # RoyalTitleThought.xml — thought labels / descriptions
    ("<label>\u6210\u4e3a\u638c\u95e8</label>",
     "<label>Became Sect Master</label>"),
    ("<description>\u6211\u73b0\u5728\u5df2\u7ecf\u662f\u638c\u95e8\u4e86</description>",
     "<description>I am now the Sect Master</description>"),
    ("<label>\u83b7\u5f97 {TITLE} \u5934\u8854</label>",
     "<label>Gained {TITLE} title</label>"),
    ("<description>\u6211\u73b0\u5728\u5df2\u7ecf\u662f{TITLE}\u4e2d\u7684\u4e00\u5458\u4e86, \u8fd9\u80fd\u8ba9\u6211\u66f4\u63a5\u8fd1\u4fee\u4ed9\u4e4b\u8def\uff01</description>",
     "<description>I am now a member of {TITLE}, bringing me closer to the path of immortality!</description>"),
    ("<description>\u6362\u53e5\u8bdd\u8bf4......\u6211\u73b0\u5728\u95e8\u6d3e\u7684\u6838\u5fc3\u4e86\uff1f\u6211\u73b0\u5728\u662f\u771f\u6b63\u7684\u4fee\u4ed9\u8005\u4e86\u5417\uff1f\u6211\u662f\u5417\uff01</description>",
     "<description>In other words... I am now the core of the sect? Am I truly a cultivator now? Am I?!</description>"),
    ("<label>\u5931\u53bb {TITLE} \u5934\u8854</label>",
     "<label>Lost {TITLE} title</label>"),
    ("<description>\u6211\u4e0d\u518d\u662f{TITLE}\u4e86\uff0c\u53ef\u6076\u554a\uff01</description>",
     "<description>I am no longer {TITLE} — how infuriating!</description>"),

    # RI_Items_Books.xml — thingCategories comment "储存"
    # (handled as TRANSLATIONS key above)
]

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
    for old, new in INLINE_REPLACEMENTS:
        result = result.replace(old, new)
    if result != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main():
    defs_root = os.path.join(REPO, "Faction", "1.6", "Defs")
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
