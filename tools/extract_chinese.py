#!/usr/bin/env python3
"""
extract_chinese.py
Scans all 1.6/Defs XML files in the repo for Chinese characters and writes
translation_progress.md — a per-mod, per-file checklist.

Run from the repo root:
    python tools/extract_chinese.py
"""

import os
import re
import sys

# Chinese character ranges (CJK Unified + extensions + punctuation)
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uff00-\uffef\u3000-\u303f]+')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODS = [
    "Furniture",
    "Hairstyle",
    "Biome",
    "FiveElements",
    "Living",
    "Bizarre",
    "Faction",
    "Forge",
    "Exorcism",
    "Core",
    "CultivationPaths",
    "Ideology",
]

def find_chinese_in_file(filepath):
    """Return list of (line_number, line_text, chinese_match) for lines with Chinese."""
    hits = []
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                matches = CHINESE_RE.findall(line)
                if matches:
                    # Join all chinese fragments found on the line
                    chinese_text = " / ".join(matches)
                    hits.append((i, line.rstrip(), chinese_text))
    except Exception as e:
        hits.append((0, f"ERROR reading file: {e}", ""))
    return hits


def scan_mod(mod_name):
    """Scan a mod's 1.6/Defs directory. Returns list of (rel_path, hits)."""
    defs_dir = os.path.join(REPO_ROOT, mod_name, "1.6", "Defs")
    results = []
    if not os.path.isdir(defs_dir):
        return results
    for root, dirs, files in os.walk(defs_dir):
        dirs.sort()
        for fname in sorted(files):
            if not fname.endswith(".xml"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
            hits = find_chinese_in_file(fpath)
            if hits:
                results.append((rel, hits))
    return results


def count_total(all_mod_results):
    total = 0
    for _, file_results in all_mod_results:
        for _, hits in file_results:
            total += len(hits)
    return total


def write_progress(all_mod_results):
    out_path = os.path.join(REPO_ROOT, "translation_progress.md")
    grand_total = count_total(all_mod_results)
    done_count = 0  # nothing translated yet

    lines = []
    lines.append("# Translation Progress\n")
    lines.append(f"**Grand total untranslated strings:** {grand_total}  \n")
    lines.append(f"**Completed:** {done_count} / {grand_total}\n\n")
    lines.append("---\n\n")
    lines.append("## Legend\n")
    lines.append("- `TODO` — needs translation\n")
    lines.append("- `DONE` — translated\n\n")
    lines.append("---\n\n")

    for mod_name, file_results in all_mod_results:
        mod_total = sum(len(h) for _, h in file_results)
        lines.append(f"## {mod_name} ({mod_total} strings)\n\n")
        if not file_results:
            lines.append("_No untranslated strings found._\n\n")
            continue
        for rel_path, hits in file_results:
            lines.append(f"### `{rel_path}`\n\n")
            lines.append("| Line | Chinese | Translation | Status |\n")
            lines.append("|------|---------|-------------|--------|\n")
            for lineno, line_text, chinese in hits:
                # Escape pipe chars so table doesn't break
                chinese_esc = chinese.replace("|", "\\|")
                lines.append(f"| {lineno} | {chinese_esc} | | TODO |\n")
            lines.append("\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return out_path, grand_total


def main():
    print(f"Repo root: {REPO_ROOT}")
    all_results = []
    for mod in MODS:
        results = scan_mod(mod)
        file_count = len(results)
        string_count = sum(len(h) for _, h in results)
        print(f"  {mod:20s} — {file_count:3d} files with Chinese, {string_count:5d} strings")
        all_results.append((mod, results))

    out_path, grand_total = write_progress(all_results)
    print(f"\nWrote: {out_path}")
    print(f"Total untranslated strings: {grand_total}")


if __name__ == "__main__":
    main()
