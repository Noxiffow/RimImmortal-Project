#!/usr/bin/env python3
"""
translate_bizarre_comments.py
Replaces Chinese XML comments in Bizarre/1.6/Defs with English equivalents.
Run from repo root: python tools/translate_bizarre_comments.py
"""

import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATIONS = {
    # === AbilityDefs/AoJing.xml ===
    "\u6307\u7532": "Fingernail",
    "\u8840\u7cdc \u5c0f": "Blood guts (small)",
    "TODO \u8fd9\u4e2a\u8c8c\u4f3c\u6709\u70b9\u95ee\u9898\u9700\u8981\u4fee\u590d": "TODO: this seems to have issues that need fixing",
    "\u8840\u7ea2\u8272": "blood red",
    "\u624b\u6307/\u811a\u8dbe": "Finger/toe",
    "\u624b/\u811a": "Hand/foot",
    "\u8840\u7cdc \u4e2d": "Blood guts (medium)",
    "\u80f3\u818a/\u817f": "Arm/leg",
    "\u8840\u7cdc \u5927": "Blood guts (large)",
    "\u706b\u7597": "Fire therapy",
    "\u518d\u751f": "Regeneration",
    "\u8715\u76ae": "Molt",

    # === AbilityDefs/AoJing_Defs.xml ===
    "\u6307\u7532\u6280\u80fd": "Fingernail ability",
    "\u624b\u6307/\u811a\u8dbe\u6280\u80fd": "Finger/toe ability",
    "\u624b/\u811a\u6280\u80fd": "Hand/foot ability",
    "\u624b\u81c2/\u817f\u6280\u80fd": "Arm/leg ability",
    "\u706b\u7597\u6280\u80fd": "Fire therapy ability",
    "\u518d\u751f\u6280\u80fd": "Regeneration ability",
    "\u8715\u76ae\u6280\u80fd": "Molt ability",

    # === AbilityDefs/BingJia.xml ===
    "\u5217\u9635": "Embattle",
    "\u8ba9\u4f60\u7684\u76df\u53cb\u5728\u5468\u56f4\u5217\u9635\uff0c\u589e\u52a0\u4ed6\u4eec\u7684\u6218\u6597\u529b\uff0c\u6301\u7eed6\u5c0f\u65f6": "Let your allies embattle around you, increasing their combat effectiveness, lasting 6 hours",
    "TODO \u66ff\u6362\u58f0\u97f3\u4e3a\u6012\u543c": "TODO Replace sound with roar",
    "\u8840\u6218": "Die fighting",
    "\u8fdb\u5165\u72c2\u66b4\u7684\u6218\u6597\u72b6\u6001\uff0c\u51b3\u4e0d\u6295\u964d\uff0c\u7edd\u4e0d\u540e\u9000": "Enter a berserk fighting state, never surrendering or retreating",
    "\u67d3\u715e": "Dyeing evil",
    "\u4f7f\u4e00\u4ef6\u8fd1\u6218\u6b66\u5668\u6cbe\u67d3\u715e\u6c14\uff0c\u4f7f\u7528\u8fd9\u4ef6\u6b66\u5668\u7684\u4eba\u4f1a\u53d8\u7684\u975e\u5e38\u5f3a\u5927\uff0c\u4f46\u662f\u4e5f\u4f1a\u66f4\u52a0\u5bb9\u6613\u6fc0\u6012": "Make a melee weapon tainted with evil; the user becomes very powerful but is more easily angered",
    "TODO \u58f0\u97f3\u662f\u7687\u6743\u7684": "TODO Sound is from Royalty DLC",
    "\u94c1\u9b44": "Iron soul",
    "\u5c06\u76f8\u9996": "General-in-chief",

    # === AbilityDefs/NzRI_Route.xml ===
    "\u5bf9\u5e94\u7684\u5883\u754c\u7b49\u7ea7": "Corresponding realm level",

    # === AbilityDefs/ZhengDe.xml ===
    "\u7985\u97f3": "Zen sound",
    "\u53d1\u51fa\u4e00\u58f0\u8574\u542b\u7985\u610f\u7684\u58f0\u97f3\uff0c\u4ee4\u4eba\u5e61\u7136\u9192\u609f\u3002\\n\u89e3\u9664\u8ff7\u832b\u548c\u72c2\u66b4\u72b6\u6001\uff0c\u540c\u65f6\u7565\u5fae\u589e\u52a0\u610f\u8bc6\u548c\u64cd\u4f5c": "Emit a sound containing Zen meaning, making people suddenly realize. Removes confusion and berserk state, slightly increases consciousness and manipulation",
    "\u8fd9\u4f1a\u8ba9\u4f60\u66f4\u63a5\u8fd1 \u201c\u660e\u5fc3\u201d \u8def\u7ebf": "This will bring you closer to the \"Enlightenment\" route",
    "\u5e03\u65bd": "Almsgiving",
    "\u6548\u4eff\u4f5b\u7956\uff0c\u5272\u8089\u9972\u9e70\\n \u8865\u5145\u76ee\u6807\u7684\u9971\u8179\u548c\u4f11\u606f\uff0c\u540c\u65f6\u589e\u5f3a\u76ee\u6807\u7684\u6108\u5408\u901f\u5ea6": "Imitate the ancestors, cut meat to feed the eagle; supplement the target's fullness and rest, enhancing their healing speed",
    "\u8fd9\u4e2a\u4f1a\u8ba9\u4f60\u66f4\u63a5\u8fd1 \u201c\u820d\u8eab\u201d \u8def\u7ebf": "This will bring you closer to the \"Sacrifice\" route",
    "\u53c2\u7985": "Zen meditation",
    "\u4fee\u70bc\u72b6\u6001\uff0c\u964d\u4f4e\u79fb\u901f": "Cultivation state, reduces movement speed",
    "\u5728\u884c\u8d70\u5750\u5367\u4e2d\uff0c\u53c2\u609f\u7985\u7406\uff0c\u964d\u4f4e\u79fb\u52a8\u901f\u5ea6\uff0c\u4f46\u662f\u4fee\u884c\u8fdb\u5ea6\u4f1a\u968f\u65f6\u95f4\u4e0a\u5347\\n\\n \u5176\u4ed6\u7279\u6b8a\u80fd\u529b\u4f1a\u968f\u7740\u4fee\u884c\u9010\u6e10\u89e3\u9501": "During walking, sitting and lying, meditate on Zen, reduce movement speed, but progress will increase over time; other abilities unlock with practice",
    "TODO \u52a0\u70b9\u7279\u6548": "TODO Add visual effects",
    "\u5982\u6765": "Tathagata",
    "\u77ed\u65f6\u95f4\u5316\u8eab\u4e94\u667a\u5982\u6765\uff0c\u6301\u7eed\u65f6\u95f4\u5185\uff0c\u4f53\u578b\u589e\u5927\uff0c\u666e\u653b\u5e26\u8303\u56f4\u4f24\u5bb3\uff0c\u627f\u4f24 0%\uff0c\u4e0d\u53ef\u963b\u6321\uff0c\u5fc3\u7075\u654f\u611f\u5ea60%": "Briefly embody the Five Wisdom Tathagatas: enlarged body, AoE basic attacks, 0% damage taken, unstoppable, 0% psychic sensitivity",

    # === AbilityDefs/ZhengDe_Enlightenment.xml ===
    "\u6012\u89c6": "Stare angrily",
    "\u6124\u6012\u7684\u6ce8\u91ca\u76ee\u6807\uff0c\u9020\u6210\u706b\u4e0e\u7535\u4f24\u5bb3\u3002 \u201c\u6012\u76ee\u91d1\u521a\u778b\u76ee\u89c6\uff0c\u6076\u5239\u5996\u9b54\u7686\u80c6\u88c2\u3002\u201d": "Angry gaze at the target, causing fire and electric damage. \"The angry eyes of the Vajra frighten all evil demons.\"",
    "TODO \u66ff\u6362\u58f0\u97f3": "TODO Replace sound",
    "\u72ee\u5b50\u543c": "Lion's roar",
    "\u53d1\u51fa\u4e00\u58f0\u6d2a\u4eae\u7684\u543c\u53eb\uff0c\u9707\u6151\u5bf9\u65b9\uff0c\u8ba9\u5bf9\u65b9\u745f\u745f\u53d1\u6296\uff0c\u751a\u81f3\u65e0\u6cd5\u63e1\u4f4f\u81ea\u5df1\u7684\u6b66\u5668": "Make a loud roar, intimidating the opponent and making them tremble, unable to hold their weapon",
    "\u6b66\u5668\u8131\u624b \u64cd\u4f5c\u6e05\u96f6 3\u79d2": "Weapon drop: clears manipulation for 3 seconds",
    "\u5934\u6655\u8033\u9e23 \u964d\u4f4e\u89c6\u529b\u542c\u529b\u64cd\u4f5c \u4e00\u5c0f\u65f6": "Dizziness and tinnitus: reduces sight, hearing, manipulation for one hour",
    "TODO \u66ff\u6362\u58f0\u97f3(\u590d\u5236\u8fd1\u6218\u4e13\u5bb6\u543c\u53eb)": "TODO Replace sound (copy melee specialist roar)",
    "\u6167\u773c": "Keen eye",
    "\u4e4b\u540e\u52a0\u4e0a\u91d1\u5c5e\u5f02\u5f62\u7684\u68c0\u6d4b\u673a\u5236": "Add xenogerm detection mechanism later",
    "\u68b5\u754c": "Brahma area",
    "\u76fe\u5305": "Shield pack",
    "\u6280\u80fd\uff1a\u8f7b\u8e0f\u5730\u9762\uff0c\u6491\u8d77\u4e00\u7247\u4fdd\u62a4\u6027\u7684\u9886\u57df\u3002\"\u8f7b\u8e0f\u5764\u8206\u5c55\u5999\u573a\uff0c\u62a4\u6301\u4fe1\u4f17\u610f\u60a0\u957f\u3002\u4f5b\u5fc3\u5316\u4f5c\u906e\u707e\u57df\uff0c\u4e0d\u89c1\u5175\u6208\u5165\u6b64\u7586\"": "Ability: step lightly, erect a protective field. \"Lightly stepping on the ground, protecting the believers; the Buddha's heart forms a disaster shield, weapons cannot enter.\"",
    "\u751f\u6210\u6307\u5b9a\u7269\u4f53": "Spawn specified thing",
    "\u64ad\u653e\u7279\u6548": "Play visual effect",
    "\u5706\u5149\u817f": "Divine light kick",
    "\u8e22\u51fa\u4e00\u9053\u6d41\u5149\uff0c\u60e9\u6212\u547d\u4e2d\u7684\u76ee\u6807\uff0c\u88ab\u51fb\u4e2d\u7684\u76ee\u6807\u4f1a\u88ab\u6ce8\u5165\u4e00\u9053\u6cd5\u529b\uff0c\u8fd9\u9053\u6cd5\u529b\u4f1a\u5e72\u6270\u76ee\u6807\u7684\u8eab\u4f53\u52a8\u4f5c": "Kick out a stream of light, punishing the target hit; the target is injected with qi that interferes with their body movements",
    "TODO \u4fee\u6539\u58f0\u97f3": "TODO Modify sound",
    "TODO \u4fee\u6539\u4e3a\u4e13\u6709\u7279\u6548": "TODO Change to custom effect",
    "\u6148\u60b2\u638c": "Merciful hit",
    "\u4f7f\u7528\u5de7\u52b2\u653b\u51fb\u5bf9\u65b9\uff0c\u5c1d\u8bd5\u6253\u6655\u76ee\u6807": "Use skill to attack the opponent, trying to stun the target",
    "\u64bc\u5c71\u62f3": "Shake mountain fist",
    "\u84c4\u529b\u5e76\u6253\u51fa\u91cd\u5982\u5c71\u5cb3\u7684\u4e00\u62f3\uff0c\u5bf9\u654c\u4eba\u9020\u6210\u5927\u91cf\u4f24\u5bb3": "Charge and hit a punch as heavy as a mountain, causing a lot of damage to the enemy",
    "\u629a\u9876": "Touch head",
    "\u629a\u6478\u5bf9\u65b9\u7684\u5934\u90e8\uff0c\u4f7f\u7528\u6cd5\u529b\u5e87\u62a4\u5bf9\u65b9": "Touch the opponent's head, use Qi to protect them",

    # === AbilityDefs/ZhengDe_Sacrifice.xml ===
    "\u62c9\u62fd": "Dragging",
    "\u8ba9\u817f\u90e8\u626d\u66f2\u53d8\u957f\uff0c\u62d6\u62fd\u4e00\u4e2a\u4eba\u5230\u81ea\u5df1\u9762\u524d": "Let the legs twist and elongate, dragging a person in front of you",
    "\u626b\u5802\u817f": "Leg sweep",
    "\u67af\u8d25\u817f\u4f38\u5c55\u5ef6\u957f\uff0c\u5e76\u5728\u5468\u56f4\u9020\u6210\u4e00\u6b21\u5207\u5272\u4f24\u5bb3\uff0c\u7531\u4e8e\u4f4d\u7f6e\u8f83\u4f4e\uff0c\u66f4\u5927\u6982\u7387\u5bf9\u654c\u4eba\u7684\u817f\u90e8\u9020\u6210\u4f24\u5bb3,\u751a\u81f3\u53ef\u80fd\u4f1a\u5207\u65ad\u5b83\u4eec": "The withered leg extends, dealing cutting damage in range. Due to the low position, it has a higher chance of hitting enemy legs, potentially severing them",
    "\u6050\u6016\u5636\u543c": "Terror scream",
    "\u53d1\u51fa\u4e00\u58f0\u6050\u6016\u7684\u543c\u53eb\uff0c\u6050\u5413\u654c\u4eba\uff0c\u964d\u4f4e\u5176\u79fb\u52a8\u548c\u653b\u51fb\u901f\u5ea6": "Emit a terrifying roar, scaring enemies and reducing their movement and attack speed",
    "TODO \u66ff\u6362\u4e3a\u543c\u53eb": "TODO Replace with roar",
    "\u5669\u68a6\u51dd\u89c6": "Nightmare gaze",
    "\u51b0\u51b7\u7684\u51dd\u89c6\uff0c\u5c06\u626d\u66f2\u4e0e\u75af\u72c2\u6ce8\u5165\u76ee\u6807\u7684\u5fc3\u7075\u4e0e\u5904\u7406\u5668\uff0c\u5373\u4f7f\u662f\u673a\u5668\u90fd\u4f1a\u53d1\u75af": "The cold gaze injects distortion and madness into the target's mind and processor; even machines will go crazy",
    "\u89e6\u987b\u7a81\u523a": "Tentacle stab",
    "\u8ba9\u89e6\u987b\u4e2d\u7684\u6d3b\u94c1\u77ac\u95f4\u786c\u5316\uff0c\u5bf9\u654c\u4eba\u7684\u5fc3\u810f\u9020\u6210\u81f4\u547d\u4e00\u51fb": "The bioferrite in the tentacles hardens instantly, dealing a fatal blow to the enemy's heart",
    "\u89e6\u987b\u6325\u780d": "Tentacle slash",
    "\u8ba9\u89e6\u987b\u4e2d\u7684\u6d3b\u94c1\u77ac\u95f4\u786c\u5316\uff0c\u5bf9\u8303\u56f4\u5185\u7684\u654c\u4eba\u8fdb\u884c\u4e00\u6b21\u6325\u780d": "The bioferrite in the tentacles hardens instantly, slashing all enemies in range",

    # === AbilityDefs/ZhengDe_Tathagata.xml ===
    "\u5982\u6765\u5f62\u6001\u6280\u80fd": "Tathagata form abilities",
    "\u624b\u653b\u51fb - \u63e1\u788e": "Hand attack - Crush grip",
    "\u624b\u653b\u51fb - \u98de\u63b7 \u5982\u679c\u76ee\u6807\u4f4d\u7f6e\u6709\u4e1c\u897f\uff0c\u5219\u4e24\u8005\u90fd\u9020\u6210\u4f24\u5bb3": "Hand attack - Throw. If something is at the target location, both take damage",
    "\u817f\u90e8\u653b\u51fb - \u91cd\u8e0f(\u5c0f\u8303\u56f4\u6253\u98de\uff0c\u51fb\u5012)": "Leg attack - Heavy stomp (small AoE knockback and knockdown)",

    # === AbilityDefs/ZuoWang.xml ===
    "\u820c\u707f\u83b2\u82b1 (\u7fa4\u4f53\u82b1\u8a00\u5de7\u8bed)": "Tongue blooming lotus (group sweet talk)",
    "\u82b1\u8a00\u5de7\u8bed": "Sweet talk",
    "\u6df7\u73e0\u8bf3\u53d6": "Counterfeit trade",
    "\u674e\u4ee3\u6843\u50f5": "Scapegoat",
    "\u8ff7\u9635\u5e03\u65bd": "Illusion array blessing",
    "\u7f54\u5929\u5b9d\u8bf0": "Invoke deity",
    "\u7075\u4e39\u5999\u836f": "Miraculous cure",
    "\u5316\u865a\u4e3a\u5b9e": "Fiction to reality",
    "\u955c\u4e2d\u4e4b\u7269": "Reflection in a mirror",

    # === AbilityDefs/ZuoWang_Defs.xml ===
    "\u4ed9\u8def\u7269\u54c1": "RimImmortal items",
    "\u795e\u673a\u5929\u7eb5": "Forge mod items",
    "\u86a9\u5c24\u6012\u708e\u621f\u3010\u4e00\u54c1\u3011": "Chiyou's rage flame halberd [First rank]",
    "\u76d8\u9f99\u901a\u5929\u68cd\u3010\u4e00\u54c1\u3011": "Coiled dragon celestial staff [First rank]",
    "\u7409\u7483\u73cd\u73e0\u4f1e\u3010\u4e00\u54c1\u3011": "Glass pearl umbrella [First rank]",
    "\u7834\u519b\u5251\u3010\u4e00\u54c1\u3011": "Pojun sword [First rank]",
    "\u65a9\u4ed9\u5251\u3010\u4e00\u54c1\u3011": "Immortal slaying sword [First rank]",
    "\u96f7\u9706\u8fde\u73e0\u94f3\u3010\u4e00\u54c1\u3011": "Thunder pearl cannon [First rank]",
    "\u971c\u534e\u5f13\u3010\u4e00\u54c1\u3011": "Frost luminance bow [First rank]",
    "\u91d1\u94b5\u3010\u4e00\u54c1\u3011": "Golden bowl [First rank]",
    "\u6346\u4ed9\u7ef3\u3010\u4e00\u54c1\u3011": "Immortal binding rope [First rank]",
    "\u7d2b\u91d1\u846b\u82a6\u3010\u4e00\u54c1\u3011": "Purple golden gourd [First rank]",
    "\u4e09\u738b\u73b2\u73d1\u5854\u3010\u4e00\u54c1\u3011": "Three kings exquisite pagoda [First rank]",
    "\u767d\u7389\u74f6\u3010\u4e00\u54c1\u3011": "White jade vase [First rank]",
    "\u539f\u7248\u7269\u54c1": "Vanilla items",
    "\u62a4\u76fe\u8170\u5e26": "Shield belt",
    "\u542f\u7075\u88c5\u7f6e": "Psychic amplifier",
    "\u9b54\u9b3c\u7d20": "Luciferium",
    "\u5fc3\u7075\u629a\u6170\u8109\u51b2\u53d1\u751f\u5668": "Psychic soothe pulser",
    "\u52a8\u7269\u5fc3\u7075\u8109\u51b2\u53d1\u751f\u5668": "Psychic animal pulser",
    "\u4eba\u683c\u6838\u5fc3": "AI persona core",
    "\u79d1\u6280\u6838\u5fc3": "Techprof subpersona core",
    "\u6587\u5316\u7269\u54c1": "Ideology DLC items",
    "\u7687\u6743\u7269\u54c1": "Royalty DLC items",
    "\u5fc3\u7075\u6743\u6756": "Psyfocus staff",
    "\u5355\u5206\u5b50\u5251": "Mono sword",
    "\u7b49\u79bb\u5b50\u5251": "Plasma sword",
    "\u9a91\u58eb\u88c5\u7532": "Knight armor cataphract",
    "\u8098\u5203": "Elbow blade",
    "\u5fc3\u7075\u540c\u8c03\u88c5\u7f6e": "Psychic harmonizer",
    "\u5fc3\u7075\u654f\u5316\u88c5\u7f6e": "Psychic sensitizer",
    "\u62a4\u76fe\u6838\u5fc3": "Broadshield core",
    "\u4fbf\u643a\u76fe\u5305": "Pack broadshield",
    "\u751f\u7269\u79d1\u6280": "Biotech DLC items",
    "\u8d85\u51e1\u80f6\u56ca": "Archite capsule",
    "\u96c6\u6210\u5934\u5957": "Integrator headset",
    "\u8fdc\u7a0b\u4fee\u590d\u673a\u68b0\u4f53": "Remote repairer",
    "\u673a\u63a7\u4e2d\u67a2": "Mechlink",
    "\u673a\u68b0\u6307\u6325\u5b98\u5934\u76d4": "Mech commander helmet",
    "\u5730\u72f1\u7403\u70ae": "Hellsphere cannon",
    "\u9ad8\u7ea7\u6b21\u5143\u6838\u5fc3": "Subcore high",
    "\u5f02\u8c61": "Anomaly DLC items",
    "\u8d85\u51e1\u98df\u5c38\u9b3c\u590d\u6d3b\u8840\u6e05\u80f6\u56ca": "Archite ghoul resurrection serum",
    "\u53e4\u4ee3\u5fc3\u7075\u3002\u3002\u3002": "Ancient psychic shard animal pulser",
    "\u6b7b\u7075\u80cc\u5305": "Shell deadlife",

    # === DamageDefs/Damage.xml ===
    "\u8113\u75ae\u6253\u51fb": "Pustule strike",

    # === Effects/Effecter_Zd.xml ===
    "\u521d\u59cb\u5927\u5c0f\u4e3a0.1\uff0c\u6700\u5927\u5927\u5c0f\u4e3a2.0": "Initial size 0.1, maximum size 2.0",
    "\u8bbe\u7f6e\u589e\u957f\u7387": "Set growth rate",
    "\u8bbe\u7f6e\u901f\u5ea6\uff0c\u4f7f\u5176\u53d1\u5c04\u51fa\u53bb": "Set speed to launch",
    "\u521d\u59cb\u5927\u5c0f\u4e3a1.0\uff0c\u6700\u5927\u5927\u5c0f\u4e3a2.0": "Initial size 1.0, maximum size 2.0",
    "\u4f7f\u7528\u89d2\u5ea6\u6765\u8ba1\u7b97\u901f\u5ea6": "Use angle to calculate velocity",
    "\u4f7f\u7528\u652f\u6301\u900f\u660e\u5ea6\u7684\u7740\u8272\u5668": "Use transparency-compatible shader",
    "\u66ff\u6362\u4e3a\u4f60\u7684\u7eb9\u7406\u8def\u5f84": "Replace with your texture path",
    "\u4f7f\u5176\u671d\u5411\u79fb\u52a8\u65b9\u5411\u65cb\u8f6c": "Rotate towards movement direction",

    # === Effects/Motes.xml ===
    "\u6b63\u5fb7\u5bfa \u7985\u97f3 \u6280\u80fd \u7279\u6548/\u529f\u80fd Mote": "Zhengde — zen sound ability effect mote",
    "\u6b63\u5fb7\u5bfa \u62d6\u62fd\u6280\u80fd \u7ef3\u5b50\u7279\u6548 Mote": "Zhengde — drag ability rope effect mote",
    "\u6b63\u5fb7\u5bfa \u626b\u5802\u817f \u65cb\u8f6c\u7279\u6548 Mote": "Zhengde — leg sweep rotating effect mote",

    # === HediffDefs/AoJing.xml ===
    "\u5267\u75db": "Agony",
    "\u767b\u9636": "Ascend",

    # === HediffDefs/BingJia.xml ===
    "\u6b7b\u6218": "Die fighting",
    "TODO \u6839\u636e\u4e0d\u540c\u5883\u754c\u8bbe\u8ba1\u4e0d\u540c\u7684\u5f3a\u5ea6": "TODO Design different intensities per realm",
    "\u5f85\u6218": "Standby",

    # === HediffDefs/ZhengDe.xml ===
    "\u6b63\u5fb7 \u679c\u4f4d(\u4fee\u884c\u8fdb\u5ea6)": "Zhengde fruition (cultivation progress)",
    "\u6b63\u5fb7 \u4fee\u884c\u4e2d": "Zhengde — cultivation in progress",
    "\u542c\u5230\u4e86\u7985\u97f3, \u611f\u5230\u5185\u5fc3\u5e73\u9759": "Heard the zen sound, feeling calm",
    "\u5e03\u65bdHediff": "Almsgiving hediff",
    "\u63a5\u53d7\u4e86\u5582\u517b": "Accepted feeding",
    "\u8bc6\u771f": "Recognize truth",
    "\u7981\u9522": "Imprisonment",
    "\u53d7\u5230\u7981\u9522": "Imprisoned",
    "\u68a6\u9b47\u51dd\u89c6": "Dream phantom gaze",
    "\u68a6\u9b47\u51dd\u89c6": "Dream phantom gaze",
    "\u4e0d\u52a8\u5982\u5c71": "Unshakeable",
    "\u4f5b\u6cd5\u62a4\u4f51\uff0c\u4f3c\u6709\u795e\u5e87\uff0c\u90aa\u795f\u96be\u4fb5": "Buddhist protection — feels divinely sheltered, evil spirits cannot intrude",
    "TODO \u6dfb\u52a0\u62a4\u76fe\u8d34\u56fe": "TODO Add shield texture",
    "\u5934\u6655\u8033\u9e23": "Dizziness and tinnitus",
    "\u88ab\u5de8\u5927\u7684\u58f0\u97f3\u9707\u5f97\u5934\u6655\u8033\u9e23": "Struck by a huge sound, dizzy with ringing ears",
    "\u5175\u5668\u8131\u624b": "Weapon drop",
    "\u51e0\u4e4e\u65e0\u6cd5\u63e1\u4f4f\u5175\u5668": "Almost unable to grip weapon",
    "\u542c\u5230\u4e86\u6050\u6016\u7684\u543c\u53eb\uff0c\u611f\u5230\u6050\u60e7": "Heard the terrifying scream, feeling fear",
    "30\u79d2\u540e\u6d88\u5931": "Disappears after 30 seconds",
    "\u9020\u6210\u6050\u60e7": "Causes fear",
    "\u611f\u89c9\u88ab\u4e00\u4e2a\u6050\u6016\u7684\u5b58\u5728\u76ef\u4e0a\uff0c\u773c\u4e2d/\u4f20\u611f\u5668\u4e2d\u4f20\u6765\u7684\u4e00\u5207\uff0c\u90fd\u53d8\u6210\u4e86\u626d\u66f2\u7684\u5e7b\u8c61": "Feeling watched by a terrifying entity — everything in your eyes/sensors becomes a distorted illusion",
    "\u9020\u6210\u5d29\u6e83": "Causes breakdown",
    "\u8113\u75ae\u8986\u76d6": "Pustule corrosion",
    "\u88ab\u8113\u75ae\u8986\u76d6\uff0c\u611f\u5230\u5267\u70c8\u7684\u6076\u5fc3": "Covered by pustules, feeling intense nausea",
    "\u6839\u636e\u6d53\u5ea6\uff0c\u6bcf\u9694\u4e00\u6bb5\u65f6\u95f4\u4e4b\u540e\u4f1a\u5455\u5410": "Will vomit at intervals based on concentration",
    "\u5c06\u89c6\u529b\u6700\u5927\u503c\u8bbe\u7f6e\u4e3a 0.5": "Set maximum sight to 0.5",
    "\u5c06\u542c\u529b\u6700\u5927\u503c\u8bbe\u7f6e\u4e3a 0.5": "Set maximum hearing to 0.5",
    "\u5c06\u64cd\u4f5c\u6700\u5927\u503c\u8bbe\u7f6e\u4e3a 0.5": "Set maximum manipulation to 0.5",

    # === HediffDefs/ZhengDe_Defs.xml ===
    "\u6b63\u5fb7\u5bfa \u514b\u5df1\u7ebf": "Zhengde temple — restraint line",
    "\u6b63\u5fb7\u5bfa \u660e\u5fc3\u7ebf": "Zhengde temple — enlightenment line",
    "\u6b63\u5fb7\u5bfa \u820d\u8eab\u7ebf": "Zhengde temple — sacrifice line",

    # === HediffDefs/ZuoWang.xml ===
    "\u975e\u7f61": "FeiGang",
    "\u9ebb\u5c06\u724c": "Mahjong tiles",
    "\u7f8e\u597d\u5e7b\u666f": "Fantasy world",
    "\u7f8e\u597d\u56de\u5fc6": "Beautiful memory",
    "\u5fc3\u667a\u6b8b\u7f3a(\u5fc3\u667a\u88ab\u5207\u5272)": "Mental deficiency (mind cut)",

    # === HediffDefs/BodyParts/Tags.xml ===
    "\u5750\u5fd8\u9053 \u5fc3\u7d20 \u8eab\u4f53\u90e8\u4ef6": "Zuowang — Xinsu body parts",
    "\u6b63\u5fb7\u5bfa \u8eab\u4f53\u90e8\u4ef6": "Zhengde temple body parts",
    "\u6b63\u5fb7\u5bfa \u514b\u5df1": "Zhengde temple — restraint",
    "\u6b63\u5fb7\u5bfa \u660e\u5fc3": "Zhengde temple — enlightenment",
    "\u6b63\u5fb7\u5bfa \u820d\u8eab": "Zhengde temple — sacrifice",

    # === HediffDefs/BodyParts/ZhengDe_Enlightenment.xml ===
    "\u660e\u5fc3\u76f8\u5173\u8eab\u4f53\u90e8\u4ef6": "Enlightenment-related body parts",
    "\u83e9\u63d0\u5fc3": "Bodhisattva heart",
    "\u7279\u6548\uff1a\u8111\u540e\u5149\u73af\u4f5b\u73e0": "Effect: Buddha bead halo behind head",
    "\u5149\u73af\uff1a\u83e9\u63d0: \u8303\u56f4\u5185\u53cb\u65b9\u51cf\u4f24\u52a0\u62a4\u7532": "Halo — Bodhi: friendly units in range take less damage and gain armor",
    "\u68b5\u9e23\u80ba": "Thunder lung",
    "\u72ee\u5b50\u543c \u8303\u56f4\u964d\u4f4e\u89c6\u529b\u542c\u529b\u64cd\u4f5c": "Lion's roar — reduces sight, hearing, manipulation in range",
    "\u4f34\u968f\u7740\u6bcf\u4e00\u6b21\u547c\u5438\uff0c\u4f3c\u4e4e\u90fd\u6709\u9690\u9690\u7684\u4f5b\u7ecf\u5ff5\u9882\u58f0\uff0c\u5f53\u5927\u58f0\u543c\u53eb\u65f6\uff0c\u4e00\u5b9a\u80fd\u9707\u6151\u4f17\u751f\u5427\u3002 \u9644\u52a0\u80fd\u529b\uff1a\u72ee\u5b50\u543c": "With every breath, faint sutra chanting seems to echo. When you shout loudly, all living beings will be intimidated. Additional ability: 'lion's roar'",
    "\u6012\u76ee": "Glaring eye",
    "\u8303\u56f4\u706b\u7130\\EMP\u52a0\u7206\u70b8": "Range flame/EMP plus explosion",
    "\u770b\u4f3c\u6148\u7709\u5584\u76ee\uff0c\u7136\u800c\u9690\u9690\u4e5f\u6709\u4e1d\u4e1d\u706b\u5149\u95ea\u70c1\u3002\"\u4f5b\u867d\u6148\u60b2\u4ea6\u6709\u6012\uff0c\u4e09\u5206\u706b\u6027\u9690\u5fc3\u4e2d\u3002\" \u9644\u52a0\u80fd\u529b\uff1a\u6012\u76ee": "It looks like a kind face, but there are faint flashes of fire. 'Although the Buddha is compassionate, there is also anger hidden within.' Additional ability: 'stare angrily'",
    "\u65e0\u52a8\u81c2": "Unshakeable arm",
    "\u89e6\u6478\u76ee\u6807\uff0c\u6dfb\u52a0\u51cf\u4f24hediff\uff0c\u5957\u76fe": "Touch target, add damage reduction hediff, apply shield",
    "\u808c\u8089\u575a\u5b9e\uff0c\u5982\u540c\u77f3\u5934\u4e00\u822c\uff0c\u7ed9\u4eba\u4ee5\u5341\u8db3\u7684\u5b89\u5168\u611f\u3002 \u9644\u52a0\u80fd\u529b\uff1a\u629a\u9876": "Muscles solid as stone, giving a strong sense of security. Additional ability: 'touching head'",
    "\u91d1\u521a\u81c2": "Vajra arm",
    "\u6253\u6655\uff0c\u51fb\u5012": "Knockout, knockdown",
    "\u808c\u8089\u866c\u7ed3\uff0c\u8868\u9762\u9690\u9690\u6d41\u5149\u95ea\u70c1\uff0c\u5982\u540c\u91d1\u521a\u77f3\u4e00\u822c\u3002 \u9644\u52a0\u80fd\u529b\uff1a\u64bc\u5c71\u62f3\uff0c\u6148\u60b2\u638c": "Muscles knotted, faintly shining like a diamond. Additional abilities: 'shake mountain fist', 'merciful hit'",
    "\u8e22\u51fa\u6d41\u5149,\u5927\u6247\u5f62\u5207\u5272\u4f4e\u4f24\u5bb3,stuck,": "Kick out a stream of light, large fan-shaped cut, low damage, stuck",
    "\u8e29\u5728\u5730\u4e0a\u65f6\uff0c\u5730\u9762\u4eff\u82e5\u6c34\u9762\u4e00\u6837\u6cdb\u51fa\u6d9f\u6f2a\uff0c\u4ed4\u7ec6\u4e00\u89c2\uff0c\u4f3c\u4e4e\u53c8\u4ec0\u4e48\u90fd\u6ca1\u6709\u3002\\n\\n \u9644\u52a0\u80fd\u529b\uff1a\u5706\u5149\u817f": "Stepping on the ground, it ripples like water. Upon closer inspection, nothing seems to be there. Additional ability: 'divine light kick'",
    "\u83b2\u82b1\u817f": "Lotus leg",
    "\u82b1\u5f00\u89c1\u4f5b\uff0c\u6b65\u6b65\u751f\u83b2\u3002\\n\\n \u9644\u52a0\u80fd\u529b\uff1a\u68b5\u754c": "Flowers bloom to see the Buddha, lotus blossoms with each step. Additional ability: 'brahma area'",

    # === HediffDefs/BodyParts/ZhengDe_Restraint.xml ===
    "\u514b\u5df1\u76f8\u5173\u8eab\u4f53\u90e8\u4ef6": "Restraint-related body parts",
    "\u65e0\u91cf\u5fc3": "Boundless heart",
    "\u7279\u6548\uff1a\u8111\u540e\u5149\u73af": "Effect: Halo behind head",
    "\u5149\u73af: \u5b9e\u5e72:\u8303\u56f4\u5185\u52a0\u5de5\u4f5c\u6548\u7387,\u82e6\u884c:\u964d\u4f4e\u9965\u997f\u4f11\u606f\u9700\u6c42": "Halo — diligence: increase work efficiency in range; asceticism: reduce hunger and rest requirements",
    "\u591c\u89c6\uff0c\u6280\u80fd\uff0c\u79fb\u9664\u9690\u5f62\uff0c\u82e5\u6709DLC\uff0c\u987a\u4fbf\u79fb\u9664\u9ed1\u6697\u7075\u80fd\u9690\u5f62": "Night vision, ability, remove invisibility; if DLC, also remove dark psychic invisibility",
    "\u5f97\u6167\u773c\uff0c\u4e0d\u89c1\u4f17\u751f\uff0c\u5c3d\u706d\u4e00\u5f02\u76f8": "With discerning eyes, all beings are unseen, all differences extinguished",
    "TODO \u4e0d\u53d7\u9ed1\u6697\u5f71\u54cd": "TODO Unaffected by darkness",
    "\u8fa9\u624d\u820c": "Eloquence tongue",
    "\u4ea4\u6613\u3001\u4f20\u6559\u76f8\u5173\u7cfb\u6570": "Trade and preaching coefficients",
    "\u201c\u83e9\u63d0\u672c\u65e0\u6811\uff0c\u660e\u955c\u4ea6\u975e\u53f0\u201d": "\"Bodhi is not a tree, the mirror has no stand\"",
    "\u658b\u85cf\u80c3": "Asceticism stomach",
    "\u514d\u75ab\u98df\u7269\u4e2d\u6bd2\uff0c\u6bd2\u7d20hediff\u514d\u75ab\uff0c\u6210\u763e\u514d\u75ab": "Immune to food poisoning, toxin hediffs, and addiction",
    "\u4e00\u5207\u6709\u4e3a\u6cd5\uff0c\u5982\u68a6\u5e7b\u6ce1\u5f71\uff0c\u5982\u9732\u4ea6\u5982\u7535\uff0c\u5e94\u4f5c\u5982\u662f\u89c2": "All material things are like dreams and bubbles, like dew and lightning, and should be viewed as such",
    "\u98df\u7269\u4e2d\u6bd2\u51e0\u7387": "Food poisoning chance",
    "\u6bd2\u7d20\u62b5\u6297": "Toxin resistance",
    "\u514d\u75ab\u539f\u7248\u6210\u763e\u54c1": "Immune to vanilla addictions",
    "\u7b03\u884c\u817f": "Devote leg",
    "\u4e0d\u53ef\u963b\u6321": "Unstoppable",
    "\u201c\u6b32\u901f\u5219\u4e0d\u8fbe\u3002\u201d\u4fee\u884c\u5982\u540c\u6500\u767b\u9ad8\u5cf0\uff0c\u9700\u4e00\u6b65\u4e00\u4e2a\u811a\u5370\uff0c\u7a33\u5065\u524d\u884c\u3002\u82e5\u8d2a\u56fe\u6377\u5f84\uff0c\u5f80\u5f80\u4f1a\u5bfc\u81f4\u6839\u57fa\u4e0d\u7a33": "\"More haste, less speed.\" Cultivation is like climbing a peak — steady steps forward. Seeking shortcuts often leads to an unstable foundation",
    "\u822c\u82e5\u817f": "Prajna leg",
    "\u822c\u82e5\u7684\u542b\u4e49\u662f\u8fa8\u8bc6\u667a\u6167\u3001\u8fa8\u8bc6\u624d\u667a": "Prajna means to discern wisdom and intelligence",
    "\u5f71\u54cd\u7814\u7a76\u901f\u5ea6": "Affects research speed",
    "\u5320\u5fc3\u81c2": "Craftsmanship arm",
    "\u52a0\u8d28\u91cf\u504f\u79fb(\u89c1\u624b\u5de5\u5927\u5e08)": "Add quality offset (see master craftsman)",
    "\u5fc3\u5982\u5de5\u753b\u5e08\uff0c\u80fd\u753b\u8bf8\u4e16\u95f4\u3002\u4e94\u8574\u6089\u4ece\u751f\uff0c\u65e0\u6cd5\u800c\u4e0d\u9020\u3002": "Our mind is like a painter, capable of painting all the images of the world. The five aggregates all arise from this, and no dharma cannot be created.",
    "\u6211\u4eec\u7684\u5fc3\u5982\u540c\u753b\u5e08\uff0c\u80fd\u591f\u7ed8\u5236\u51fa\u4e16\u95f4\u4e07\u8c61\uff0c\u800c\u4fee\u884c\u6b63\u662f\u8981\u63cf\u7ed8\u51fa\u5185\u5fc3\u7684\u6e05\u51c0\u4e0e\u667a\u6167\u3002": "Our mind is like a painter, capable of painting all the world's images; meditation precisely paints the purity and wisdom of the heart.",
    "\u5236\u9020\u8d28\u91cf\u504f\u79fb": "Production quality offset",
    "\u52e4\u5de5\u81c2": "Diligence arm",
    "\u5168\u5c40\u5de5\u4f5c\u6548\u7387\uff0c\u64cd\u4f5c": "Global work efficiency, manipulation",
    "\u4fee\u884c\u975e\u4e00\u8e74\u800c\u5c31\u4e4b\u4e8b\uff0c\u9700\u4ee5\u52e4\u52b3\u4e4b\u5fc3\uff0c\u6301\u7eed\u4e0d\u65ad\u5730\u8015\u8018\u3002": "Cultivation cannot be accomplished overnight; it requires a diligent heart and continuous effort.",
    "\u666e\u901a\u5de5\u4f5c\u901f\u5ea6": "General work speed",
    "\u7834\u89e3\u901f\u5ea6": "Hacking speed",
    "\u5efa\u9020\u901f\u5ea6": "Construction speed",
    "\u5168\u5c40\u5de5\u4f5c\u901f\u5ea6": "Global work speed",
    "\u79cd\u690d\u901f\u5ea6": "Planting speed",
    "\u6316\u6398\u901f\u5ea6": "Mining speed",

    # === HediffDefs/BodyParts/ZhengDe_Sacrifice.xml ===
    "\u820d\u8eab\u76f8\u5173\u8eab\u4f53\u90e8\u4ef6": "Sacrifice-related body parts",
    "\u6d4e\u4e16\u5fc3": "Bodhisattva heart (sacrifice)",
    "\u7279\u6548\uff1a\u8111\u540e\u8840\u8272\u8346\u68d8": "Effect: blood-colored thorns behind head",
    "\u5149\u73af: \u6218\u6817,\u964d\u4f4e\u62a4\u7532,\u627f\u4f24\u7cfb\u6570*3": "Halo — tremor, reduce armor, damage taken x3",
    "\u7329\u7ea2\u773c": "Crimson eyes",
    "\u5669\u68a6\u51dd\u89c6\uff0c\u5c0f\u8303\u56f4\u7cbe\u795e\u9519\u4e71": "Nightmare gaze, small area mental breakdown",
    "\u95ea\u70c1\u7740\u7329\u7ea2\u7684\u5149\u8292\uff0c\u8fd9\u4e0e\u4f60\u5728\u90a3\u5ea7\u53e4\u602a\u7684\u5de8\u77f3\u4e0a\u770b\u5230\u7684\u6761\u7eb9\u51e0\u4e4e\u4e00\u81f4": "Shining with crimson light, almost identical to the stripes you saw on that strange monolith",
    "\u602a\u5f02\u820c": "Strange tongue",
    "\u6050\u6016\u5636\u543c\uff0c\u8303\u56f4\u60ca\u5413": "Terror scream, range fear",
    "\u4e0a\u9762\u8986\u76d6\u4e86\u8be1\u5f02\u7684\u7eb9\u8def\uff0c\u626d\u66f2\u4eff\u82e5\u86c7\u820c\uff0c\u9690\u9690\u8fd8\u6709\u773c\u7403\u8fde\u63a5\u5728\u5176\u4e0a": "Covered with strange patterns, twisted like a snake's tongue, with faint eyeballs connected to it",
    "\u589e\u751f\u809d": "Hypertrophy liver",
    "\u5410\u51fa\u8840\u8089\u91ce\u517d": "Spit out a flesh beast",
    "\u65f6\u4e0d\u65f6\u4f20\u6765\u9690\u9690\u7684\u80c0\u75db": "Occasional dull bloating pain",
    "\u8113\u75ae\u81c2": "Abscess arm",
    "\u653b\u51fb\u9020\u6210\u6076\u5fc3": "Attacks cause nausea",
    "\u4f60\u7684\u624b\u81c2\u4e0a\u9762\u8986\u76d6\u7740\u8113\u75b1\uff0c\u5176\u4ed6\u90e8\u5206\u4e5f\u5448\u73b0\u534a\u8150\u70c2\u72b6\u6001": "Your arm is covered with pustules, with other parts in a semi-rotten state",
    "\u76d8\u5377\u81c2": "Coiled arm",
    "\u9ad8\u5207\u5272\u4f24\u5bb3": "High cutting damage",
    "\u4e00\u6761\u771f\u6b63\u7684\u89e6\u987b\uff0c\u5728\u575a\u786c\u548c\u67d4\u8f6f\u4e4b\u95f4\u5feb\u901f\u53d8\u52a8\u7740\uff0c\\n\\n\u5728'\u5927\u50a9'\u4ee5\u5916\u7684\u4e16\u754c\uff0c\u4f3c\u4e4e\u53f8\u547d'\u4e94\u667a\u5982\u6765'\u7684\u56de\u5e94\u88ab\u67d0\u79cd\u53ef\u6015\u7684\u4e1c\u897f\u622a\u53d6\u4e86": "A real tentacle that rapidly alternates between hardness and softness. Outside the world of 'DaNuo', it seems the response of the 'Five Wisdom Tathagatas' was intercepted by something terrible",
    "\u65a9\u51fb": "Slash",
    "\u523a\u7a7f": "Stab",
    "\u626d\u7ed3\u817f": "Twisted leg",
    "\u8fd9\u6761\u817f\u626d\u7ed3\u9519\u4e71\uff0c\u51e0\u4e4e\u6ca1\u6709\u9aa8\u9abc\uff0c\u5982\u89e6\u987b\u4e00\u822c\uff0c\u7f3a\u683c\u5916\u575a\u97e7\u7075\u6d3b": "This leg is twisted and disordered, nearly boneless like a tentacle, yet surprisingly tough and flexible",
    "\u67af\u8d25\u817f": "Withered leg",
    "\u5468\u56f4\u5207\u817f": "Surrounding leg cut",
    "\u8fd9\u6761\u817f\u9ed1\u7626\u67af\u5e72\uff0c\u5374\u683c\u5916\u7ed3\u5b9e\u6709\u529b\uff0c\u4e0a\u9762\u8986\u6ee1\u4e86\u4e11\u964b\u7684\u75a4\u75d5\u548c\u87ba\u7eb9\uff0c\u8fd8\u6563\u53d1\u51fa\u8150\u8089\u822c\u7684\u81ed\u5473\uff0c\u8fd8\u6709\u4e00\u79cd\u5947\u5f02\u7684\u517c\u5177\u6709\u673a\u7269\u4e0e\u91d1\u5c5e\u7684\u7279\u6027\u7684\u7ea4\u7ef4\u7269\u8d28\u70b9\u7f00\u5176\u4e2d": "This leg is black, thin, and withered yet powerfully strong. Covered in ugly scars and wrinkles, it emits a stench of rotten flesh, with a strange fiber material bearing both organic and metallic properties",

    # === HediffDefs/BodyParts/ZuoWang.xml ===
    "\u5fc3\u7d20\u7684\u773c\u955c": "Xinsu's eye",

    # === SoundDefs/ZhengDe.xml ===
    "\u8df3": "Jump",
    "\u5207\u8089": "Cut meat",
    "\u7a7a\u6325": "Swing at air",
    "\u5636\u543c": "Scream",
    "\u6050\u6016\u51dd\u89c6 TerrifyingGaze": "Terrifying gaze TerrifyingGaze",

    # === ThingDefs_Misc/Ability.xml ===
    "\u53ef\u80fd\u4f9d\u8d56DLC": "May depend on DLC",
    "\u4f9d\u8d56DLC Royalty": "Requires DLC Royalty",

    # === ThingDefs_Misc/Bionic.xml ===
    "\u5fc3\u7d20\u7684\u773c\u775b": "Xinsu's eyes",
    "\u4eff\u751f\u4f53\u57fa\u7840": "Bionic base",

    # === ThingDefs_Misc/Filth.xml ===
    "\u9178\u6027\u7c98\u6db2": "Acid mucus",

    # === ThoughtDefs/ZuoWang.xml ===
    "\u597d\u8bdd": "Good words",
    "\u65e0\u610f\u4e49\u7684\u8bdd": "Meaningless words",
    "\u597d\u5fc3\u60c5": "Good mood",
}

# Special multi-line comment in NzRI_Route.xml that contains embedded Chinese
INLINE_REPLACEMENTS = [
    # NzRI_Route.xml: commented-out Tathagata route level
    (
        "<!-- \n            \u5982\u6765\u5f62\u6001\n            <li>\n                <level>9</level>\n                <abilities>\n                    <li></li>\n                </abilities>\n            </li>-->",
        "<!-- Tathagata form (route level 9 — disabled)\n            <li>\n                <level>9</level>\n                <abilities>\n                    <li></li>\n                </abilities>\n            </li>-->",
    ),
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
    defs_root = os.path.join(REPO, "Bizarre", "1.6", "Defs")
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
