# RimImmortal — Full English Translation

This is a personal translation fork of the **RimImmortal (边缘仙路)** mod suite for RimWorld, a xianxia/cultivation themed mod collection by **TangW**.

> **Note:** This fork is for personal use pending explicit permission from the original author (TangW). Do not redistribute without authorization.

---

## Original Mods

All credit goes to the original authors. This repository contains translated copies of:

| Folder | Original Mod | Steam ID |
|--------|-------------|----------|
| `Core/` | 边缘仙路 (RimImmortal Core) | 3296476341 |
| `Exorcism/` | 边缘仙路-斩妖除魔 | 3663824172 |
| `Forge/` | 边缘仙路-仙炉锻造 | 3308873789 |
| `Faction/` | 边缘仙路-修仙门派 | 3414794353 |
| `Bizarre/` | 边缘仙路-奇异事件 | 3325655760 |
| `Living/` | 边缘仙路-修仙生活 | 3326145525 |
| `FiveElements/` | 边缘仙路-五行灵根 | 3439473215 |
| `Furniture/` | 边缘仙路-仙家家具 | 3478098371 |
| `Biome/` | 边缘仙路-仙灵秘境 | 3624919432 |
| `Hairstyle/` | 边缘仙路-发型包 | 3265157569 |
| `CultivationPaths/` | RimImmortal Cultivation Paths (local mod) | — |
| `Ideology/` | RimImmortal Ideology (local mod) | — |

---

## Translation Approach

Chinese text is embedded directly in the `Defs/` XML files of each mod. This translation edits the Defs inline, making English the base language. Chinese players are unaffected — their `Languages/ChineseSimplified/` override folders remain untouched.

**Scope:** RimWorld 1.6 only (1.5 Def folders are not translated).

---

## Translation Progress

See [`translation_progress.md`](translation_progress.md) for a full per-file, per-string checklist.

| Mod | Status |
|-----|--------|
| Furniture | TODO |
| Hairstyle | Mostly done |
| Biome | TODO |
| FiveElements | TODO |
| Living | TODO |
| Bizarre | TODO |
| Faction | TODO |
| Forge | TODO |
| Exorcism | TODO |
| Core | TODO |
| CultivationPaths | TODO |
| Ideology | TODO |

---

## Tools

- `tools/extract_chinese.py` — Scans all 1.6 Defs XML files, outputs `translation_progress.md` with every untranslated string flagged as TODO.

Run it from the repo root:
```
python tools/extract_chinese.py
```
