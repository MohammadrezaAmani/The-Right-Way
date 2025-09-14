import os
from pathlib import Path
from typing import Dict, List

APPS_DIR = Path(__file__).resolve().parent.parent / "apps"

# Map language suffix to emoji, شامل کردی و زبان‌های بیشتر
LANGS = {
    "en": "🇬🇧",
    "fa": "🇮🇷",
    "ar": "🇸🇦",
    "ku": "🇹🇯",  # کردی (به عنوان مثال پرچم تاجیکستان یا پرچم محلی)
    "de": "🇩🇪",
    "fr": "🇫🇷",
    "es": "🇪🇸",
    "it": "🇮🇹",
    "zh": "🇨🇳",
    "jp": "🇯🇵",
    "kr": "🇰🇷",
    "ru": "🇷🇺",
    "pt": "🇵🇹",
    "tr": "🇹🇷",
    "nl": "🇳🇱",
    "sv": "🇸🇪",
    "no": "🇳🇴",
    "fi": "🇫🇮",
    "hi": "🇮🇳",
    "bn": "🇧🇩",
    "ur": "🇵🇰",
    "he": "🇮🇱",
    "th": "🇹🇭",
    "vi": "🇻🇳",
}


def generate_name(name: str) -> str:
    """Convert folder/file name to readable title."""
    return str(name).replace("-", " ").replace("_", " ").replace(".", " ").title()


def find_readmes(folder: Path) -> Dict[str, str]:
    """Find all README files and map language suffix to filename."""
    readme_files = {}
    for f in folder.iterdir():
        if (
            f.is_file()
            and f.name.lower().startswith("readme")
            and f.suffix.lower() == ".md"
        ):
            parts = f.stem.lower().split(".")
            if len(parts) == 1:
                readme_files["en"] = f.name
            else:
                readme_files[parts[-1]] = f.name
    return readme_files


def generate_toc(
    folder: Path, base_folder: Path = APPS_DIR, indent: str = "  "
) -> List[str]:
    toc_lines = []
    rel_path = folder.relative_to(base_folder)
    depth = len(rel_path.parts)
    prefix = indent * depth + "- "
    folder_name = generate_name(folder.name)

    readmes = find_readmes(folder)

    if readmes:
        # لینک اصلی: ترجیح README اصلی یا en
        main_file = readmes.get("en") or next(iter(readmes.values()))
        md_line = f"{prefix}[{folder_name}](./{'/'.join(rel_path.parts)}/{main_file})"
        # اضافه کردن همه زبان‌ها
        for lang, fname in readmes.items():
            if fname != main_file:
                emoji = LANGS.get(lang, "")
                md_line += (
                    f" [{emoji}](./{'/'.join(rel_path.parts)}/{fname})"
                    if emoji
                    else f" [{fname}](./{'/'.join(rel_path.parts)}/{fname})"
                )
        toc_lines.append(md_line)
    else:
        # فولدر بدون README → لینک به مسیر خودش
        md_line = f"{prefix}[{folder_name}](./{'/'.join(rel_path.parts)})/"
        toc_lines.append(md_line)

    # زیر فولدرها
    for sub in sorted(folder.iterdir()):
        if sub.is_dir():
            toc_lines.extend(generate_toc(sub, base_folder, indent=indent))

    return toc_lines


if __name__ == "__main__":
    toc = []
    for subfolder in sorted(APPS_DIR.iterdir()):
        if subfolder.is_dir():
            toc.extend(generate_toc(subfolder, base_folder=APPS_DIR))

    print("\n".join(toc))
