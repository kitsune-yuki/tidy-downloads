# tidy-downloads

Sort a messy Downloads folder into tidy subfolders by file type — PDFs
with PDFs, photos with photos, videos with videos, code with code.

```text
Downloads/
├── report.pdf        →  Documents/report.pdf
├── photo.jpg         →  Images/photo.jpg
├── holiday.mp4       →  Videos/holiday.mp4
├── song.mp3          →  Audio/song.mp3
├── backup.zip        →  Archives/backup.zip
├── script.py         →  Code/script.py
├── setup.exe         →  Installers/setup.exe
└── mystery.xyz       →  Other/mystery.xyz
```

## Why

A Downloads folder collects everything: PDFs next to photos, installers
next to code, videos next to zip files. Finding anything means scrolling
through the mess. This script sorts the files for you, safely.

## Safety

- **Nothing is ever deleted.** Files are only moved (or copied with
  `--copy`).
- **Nothing is ever overwritten.** If a name already exists in the
  destination, the file is renamed `name (1).ext`.
- **It shows the plan first and asks before moving anything.**
  Subfolders, hidden files, and the script itself are left alone.

## Usage

Python 3.8+, standard library only — no install needed. Works on
Windows, macOS, and Linux.

```sh
# Tidy your Downloads folder (asks first)
python tidy.py

# Just see what it would do, move nothing
python tidy.py ~/Downloads --dry-run

# Tidy without asking
python tidy.py ~/Downloads --yes

# Tidy any folder
python tidy.py ~/Pictures

# Group files into YYYY-MM folders inside each category
python tidy.py ~/Downloads --by-date

# Copy instead of move
python tidy.py ~/Downloads --copy
```

## Categories

| Folder | File types |
| --- | --- |
| Images | jpg, png, gif, webp, svg, bmp, heic, tif, avif, raw, … |
| Videos | mp4, mkv, mov, avi, webm, wmv, … |
| Audio | mp3, wav, flac, aac, ogg, m4a, … |
| Documents | pdf, doc, docx, txt, md, xls, xlsx, ppt, csv, epub, … |
| Archives | zip, tar, gz, rar, 7z, … |
| Code | py, js, ts, html, css, json, sh, java, go, rs, sql, … |
| Installers | exe, msi, dmg, pkg, apk, deb, … |
| Fonts | ttf, otf, woff, woff2 |
| Other | anything it does not recognise |

## Run it regularly

Run it once a week and your Downloads folder stays tidy on its own.
On Linux or macOS you can schedule it with cron:

```sh
# Every Sunday at 09:00, tidy Downloads without asking
0 9 * * 0 python3 /path/to/tidy-downloads/tidy.py ~/Downloads --yes
```

## License

MIT — do what you like with it, just keep the license notice.
