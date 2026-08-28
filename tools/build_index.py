"""Regenerate index.json from packs/.

The revision is a hash of every pack's bytes, so editing a translation changes it
without anyone having to remember to bump a version. Clients compare the revision
and re-pull only when it differs.

Run from the repository root: python3 tools/build_index.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
INDEX = ROOT / "index.json"
REVISION_CHARS = 12
ENCODING = "utf-8"

# A language names itself the same way whatever the reader speaks, so these are
# endonyms and are never translated.
NAMES = {
    "da": "Dansk", "de": "Deutsch", "es": "Español", "fr": "Français",
    "hu": "Magyar", "nl": "Nederlands", "pt": "Português", "sv": "Svenska",
    "ja": "日本語", "zh-Hans": "简体中文", "zh-Hant": "繁體中文",
}


def main() -> None:
    packs = sorted(p for p in PACKS.glob("*.json"))
    unnamed = [p.stem for p in packs if p.stem not in NAMES]
    if unnamed:
        raise SystemExit("no endonym in NAMES for: %s" % ", ".join(unnamed))

    digest = hashlib.sha256()
    languages = []
    for pack in packs:
        raw = pack.read_bytes()
        digest.update(pack.name.encode(ENCODING))
        digest.update(raw)
        languages.append({"code": pack.stem, "name": NAMES[pack.stem], "path": "packs/%s" % pack.name})

    index = {"revision": digest.hexdigest()[:REVISION_CHARS], "languages": languages}
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding=ENCODING)
    print("index.json: %d languages, revision %s" % (len(languages), index["revision"]))


if __name__ == "__main__":
    main()
