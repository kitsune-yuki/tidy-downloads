#!/usr/bin/env python3
"""Tidy Downloads — sort a messy folder into tidy subfolders by file type.

A Downloads folder collects everything: PDFs next to photos, installers
next to code, videos next to zip files. This script sorts the files into
subfolders by type, safely:

- It never deletes anything and never overwrites a file. When a name
  already exists in the destination, the file is renamed ``name (1).ext``.
- It only moves loose files in the folder you point it at. Subfolders,
  hidden files, and the script itself are left alone.
- It shows the plan first and asks before moving anything. Use
  ``--dry-run`` to only see the plan, or ``--yes`` to skip the question.

Usage:
    python tidy.py                    # tidy ~/Downloads, ask first
    python tidy.py ~/Downloads --dry-run
    python tidy.py ~/Downloads --yes
    python tidy.py ~/Pictures --by-date   # group into 2026-11, 2026-10, ...
    python tidy.py ~/Downloads --copy     # copy instead of move

Python 3.8+, standard library only. Works on Windows, macOS, and Linux.
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "Images": {
        "jpg", "jpeg", "png", "gif", "webp", "svg", "bmp", "heic", "heif",
        "tif", "tiff", "ico", "avif", "raw",
    },
    "Videos": {
        "mp4", "mkv", "mov", "avi", "webm", "wmv", "flv", "m4v", "mpg",
        "mpeg", "3gp",
    },
    "Audio": {
        "mp3", "wav", "flac", "aac", "ogg", "m4a", "wma", "opus",
    },
    "Documents": {
        "pdf", "doc", "docx", "txt", "md", "rtf", "odt", "xls", "xlsx",
        "csv", "ppt", "pptx", "odp", "ods", "epub",
    },
    "Archives": {
        "zip", "tar", "gz", "tgz", "bz2", "xz", "rar", "7z",
    },
    "Code": {
        "py", "js", "ts", "jsx", "tsx", "html", "htm", "css", "json",
        "xml", "sh", "bat", "ps1", "java", "c", "cpp", "h", "go", "rs",
        "rb", "php", "sql", "yaml", "yml", "toml", "ipynb",
    },
    "Installers": {
        "exe", "msi", "dmg", "pkg", "apk", "deb", "rpm", "appimage",
    },
    "Fonts": {
        "ttf", "otf", "woff", "woff2",
    },
}

EXT_TO_CATEGORY = {
    ext: name for name, exts in CATEGORIES.items() for ext in exts
}


def category_of(path: Path) -> str:
    """Return the folder name for a file, or 'Other' when unknown."""
    return EXT_TO_CATEGORY.get(path.suffix.lower().lstrip("."), "Other")


def unique_destination(folder: Path, name: str) -> Path:
    """A path inside folder that does not overwrite an existing file."""
    target = folder / name
    if not target.exists():
        return target
    stem, suffix = Path(name).stem, Path(name).suffix
    n = 1
    while True:
        target = folder / f"{stem} ({n}){suffix}"
        if not target.exists():
            return target
        n += 1


def plan(folder: Path, by_date: bool):
    """List (source, destination) pairs for every loose file in folder."""
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        if item.name.startswith("."):
            continue
        if item.resolve() == Path(__file__).resolve():
            continue
        dest_folder = folder / category_of(item)
        if by_date:
            stamp = datetime.fromtimestamp(item.stat().st_mtime)
            dest_folder = dest_folder / stamp.strftime("%Y-%m")
        moves.append((item, unique_destination(dest_folder, item.name)))
    return moves


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Sort a messy folder into subfolders by file type."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="folder to tidy (default: ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only show what would happen, move nothing",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="move without asking first",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="copy files instead of moving them",
    )
    parser.add_argument(
        "--by-date",
        action="store_true",
        help="group files into YYYY-MM folders inside each category",
    )
    args = parser.parse_args(argv)

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 2

    moves = plan(folder, args.by_date)
    if not moves:
        print(f"Nothing to tidy in {folder} — already clean!")
        return 0

    action = "Copy" if args.copy else "Move"
    for source, dest in moves:
        print(f"{action}: {source.name}  ->  {dest.relative_to(folder)}")
    print(f"\n{len(moves)} file(s).")

    if args.dry_run:
        print("(dry run — nothing moved.)")
        return 0
    if not args.yes:
        answer = input("Go ahead? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Cancelled — nothing moved.")
            return 0

    for source, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if args.copy:
            shutil.copy2(source, dest)
        else:
            shutil.move(str(source), str(dest))
    print(f"Done — {len(moves)} file(s) tidied in {folder}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
