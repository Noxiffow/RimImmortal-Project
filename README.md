# RimImmortal — Full English Translation

This is a personal translation fork of the **RimImmortal (边缘仙路)** mod suite for RimWorld — a xianxia/cultivation themed mod collection originally created by **TangW (堂丸)** and collaborators.

> **Note:** This fork is for personal use pending explicit permission from the original authors. Do not redistribute without authorization.

---

## Original Authors

All credit goes to the original creators. The RimImmortal suite is the work of:

| Name | Role |
|------|------|
| **堂丸 (TangW)** | Lead developer, planning, textures, XML — Core, Hairstyle, Furniture, Exorcism, Faction, Living, Biome, Forge |
| **漆黑之梦** | Primary developer — Bizarre, FiveElements, Biome; contributor on Faction |
| **羊肉罐头 (Cannon Mutton)** | Planning, textures — Core, Forge |
| **雾雨龛灯** | Programming, sound — Core |
| **凌洛 (LingLuo)** | Programming — Core, Forge, Faction |
| **骸鸾** | Programming — Core, Faction |
| **玉米淀粉 (Corn Starch)** | Programming — Core, Forge, Faction |
| **逍逍客 (Xiao Xiao Ke)** | Programming — Forge, Living |
| **chitoseender** | Contributor — Biome |
| **滚彤洗衣机** | Contributor — Bizarre |
| **爱新觉罗-派大星** | Contributor — Core, Faction |
| **玖日长弓** | Contributor — Core, Faction |
| **咩咩** | Contributor — Faction |
| **灵能罐头** | Contributor — Core, Faction |
| **尘** | Contributor — Core, Faction |
| **天才少年金杜汩** | Contributor — Core |
| **阿米 (Amli)** | Contributor — Core |

**Community Discord:** https://discord.gg/KhDHemZxyB

---

## Original Mods

| Folder | Original Mod (Chinese name) | Steam Workshop |
|--------|-----------------------------|---------------|
| `Core/` | 边缘仙路-羽化登仙 RimImmortal-Core | [3296476341](https://steamcommunity.com/sharedfiles/filedetails/?id=3296476341) |
| `Hairstyle/` | 边缘仙路-雾鬓风鬟 RimImmortal-Hairstyle | [3265157569](https://steamcommunity.com/sharedfiles/filedetails/?id=3265157569) |
| `Forge/` | 边缘仙路-神机天纵 RimImmortal-Forge | [3308873789](https://steamcommunity.com/sharedfiles/filedetails/?id=3308873789) |
| `Bizarre/` | 边缘仙路-道诡异仙 RimImmortal-Bizarre | [3325655760](https://steamcommunity.com/sharedfiles/filedetails/?id=3325655760) |
| `Living/` | 边缘仙路-俗世仙工 RimImmortal-Living | [3326145525](https://steamcommunity.com/sharedfiles/filedetails/?id=3326145525) |
| `Faction/` | 边缘仙路-百家争鸣 RimImmortal-Faction | [3414794353](https://steamcommunity.com/sharedfiles/filedetails/?id=3414794353) |
| `FiveElements/` | 边缘仙路-五行流转 RimImmortal-FiveElements | [3439473215](https://steamcommunity.com/sharedfiles/filedetails/?id=3439473215) |
| `Furniture/` | 边缘仙路-雕梁画栋 RimImmortal-Furniture | [3478098371](https://steamcommunity.com/sharedfiles/filedetails/?id=3478098371) |
| `Biome/` | 边缘仙路-山海灵域 RimImmortal-Biome | [3624919432](https://steamcommunity.com/sharedfiles/filedetails/?id=3624919432) |
| `Exorcism/` | 边缘仙路-镇邪诛鬼 RimImmortal-Exorcism | [3663824172](https://steamcommunity.com/sharedfiles/filedetails/?id=3663824172) |
| `CultivationPaths/` | RimImmortal Cultivation Paths *(local mod)* | — |
| `Ideology/` | RimImmortal Ideology *(local mod)* | — |

---

## Translation Approach

Chinese text is embedded directly in the `Defs/` XML files of each mod. This translation edits the Defs inline, making English the base language. Chinese players are unaffected — their `Languages/ChineseSimplified/` override folders remain untouched.

**Scope:** RimWorld 1.6 only.

---

## Translation Progress

| Mod | Status |
|-----|--------|
| Furniture | ✅ Complete |
| Hairstyle | ✅ Complete |
| Biome | ✅ Complete |
| FiveElements | ✅ Complete |
| Living | ✅ Complete |
| Bizarre | ✅ Complete |
| Faction | ✅ Complete |
| Forge | 🔄 In progress |
| Exorcism | 🔄 In progress |
| Core | 🔄 In progress |
| CultivationPaths | ⬜ Not started |
| Ideology | ⬜ Not started |

---

## Tools

- `tools/extract_chinese.py` — Scans all 1.6 Defs XML files, outputs `translation_progress.md` with every untranslated string flagged as TODO.

```
python tools/extract_chinese.py
```
