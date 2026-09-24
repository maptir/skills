#!/usr/bin/env python3
"""Build the Game Guides hub page from the guides in a game-guides/ folder.

Usage:
  python build_hub.py [ROOT] [--lang th] [--strings strings.json] [--remove SLUG ...]
  python build_hub.py [ROOT] --mark-published

ROOT defaults to ./game-guides. Each guide lives in ROOT/<slug>/index.html and
follows the game-guide output contract (a full HTML document with one
<script type="application/json" id="guide-meta"> block).

What it does (standard library only):
  1. Reads every ROOT/<slug>/index.html and its guide-meta.
  2. Sorts guides into: ok, needs_upgrade (no guide-meta / not a full document /
     base64 images), too_new (contract newer than this hub supports), broken.
  3. Writes ROOT/index.html — the hub page with the manifest of ok guides baked in.
     The same file is the local hub and the Artifact page.
  4. Writes/updates ROOT/hub.json ({url, contract, mode, published}).
  5. Prints a JSON report to stdout, including `files`: the supporting-file map to
     pass to the Artifact tool — only files that changed since the last publish,
     and null for files that must be removed.

--remove SLUG      drop a guide from the hub (its folder is left alone on disk
                   but it is excluded from the manifest and its published files
                   are removed).
--restore SLUG     undo an earlier --remove.
--mark-published   after a successful Artifact publish, record the current file
                   hashes in hub.json so the next build only sends changes.
"""
import hashlib
import json
import os
import re
import sys
from html.parser import HTMLParser

SUPPORTED_CONTRACTS = {1}
REQUIRED = ["contract", "slug", "game", "variant", "title", "lang", "summary",
            "game_version", "updated", "spoiler_gate", "sources"]
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "hub-template.html")

STRINGS = {
    "en": {
        "lang": "en",
        "heading": "Game Guides",
        "dek": "Every guide you have built, in one place.",
        "search": "Search games",
        "back": "All guides",
        "standalone": "Open on its own",
        "variant": "Guide",
        "updated": "Updated",
        "version": "Version",
        "guides": "guides",
        "empty": "No guides yet.",
        "nomatch": "No game matches that search.",
        "unknown": "unknown",
    },
    "th": {
        "lang": "th",
        "heading": "Game Guides",
        "dek": "คู่มือเกมทั้งหมดที่ทำไว้ รวมไว้ที่เดียว",
        "search": "ค้นหาเกม",
        "back": "คู่มือทั้งหมด",
        "standalone": "เปิดแยกหน้า",
        "variant": "คู่มือ",
        "updated": "อัปเดต",
        "version": "เวอร์ชัน",
        "guides": "คู่มือ",
        "empty": "ยังไม่มีคู่มือ",
        "nomatch": "ไม่มีเกมที่ตรงกับคำค้น",
        "unknown": "ไม่ทราบ",
    },
}


class MetaScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self._on, self._buf = [], False, []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "guide-meta":
            self._on, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "script" and self._on:
            self.blocks.append("".join(self._buf))
            self._on = False

    def handle_data(self, data):
        if self._on:
            self._buf.append(data)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_guide(folder):
    """Return (status, meta, reasons)."""
    index = os.path.join(folder, "index.html")
    with open(index, encoding="utf-8") as f:
        src = f.read()
    reasons = []
    scan = MetaScan()
    scan.feed(src)
    meta = None
    if scan.blocks:
        try:
            meta = json.loads(scan.blocks[0])
        except json.JSONDecodeError as e:
            return "broken", None, [f"guide-meta is not valid JSON: {e}"]
    if meta is None:
        reasons.append("no guide-meta")
    if not re.match(r"\s*<!doctype html>", src, re.I) or not re.search(r"<html[^>]*\blang=", src, re.I):
        reasons.append("not a full HTML document with lang")
    if re.search(r"data:image/", src, re.I):
        reasons.append("embeds base64 images")
    if meta is None or reasons:
        return "needs_upgrade", meta, reasons
    c = meta.get("contract")
    if isinstance(c, int) and c > max(SUPPORTED_CONTRACTS):
        return "too_new", meta, [f"contract {c}; this hub supports {sorted(SUPPORTED_CONTRACTS)}"]
    missing = [k for k in REQUIRED if k not in meta]
    if missing or c not in SUPPORTED_CONTRACTS:
        return "needs_upgrade", meta, [f"guide-meta missing {', '.join(missing) or 'a supported contract'}"]
    slug = os.path.basename(os.path.normpath(folder))
    if meta["slug"] != slug:
        return "broken", meta, [f"guide-meta.slug '{meta['slug']}' differs from folder '{slug}'"]
    return "ok", meta, []


def card_fields(meta):
    keep = ["slug", "game", "variant", "title", "lang", "summary", "game_version",
            "updated", "platform"]
    out = {k: meta[k] for k in keep if k in meta}
    art = meta.get("artifact")
    if isinstance(art, dict) and art.get("url"):
        out["artifact_url"] = art["url"]
    out["has_images"] = bool(meta.get("image_credits"))
    return out


def main(argv):
    flags = [a for a in argv[1:] if a.startswith("--")]
    lang, strings_file, removes, restores = "en", None, [], []
    it = iter(argv[1:])
    positional = []
    for a in it:
        if a == "--lang":
            lang = next(it, "en")
        elif a == "--strings":
            strings_file = next(it, None)
        elif a == "--remove":
            removes.append(next(it, ""))
        elif a == "--restore":
            restores.append(next(it, ""))
        elif a == "--mark-published":
            pass
        else:
            positional.append(a)
    root = os.path.abspath(positional[0] if positional else "game-guides")
    if not os.path.isdir(root):
        print(json.dumps({"error": f"no folder {root}"}))
        return 2

    hub_path = os.path.join(root, "hub.json")
    hub = {}
    if os.path.isfile(hub_path):
        with open(hub_path, encoding="utf-8") as f:
            hub = json.load(f)
    hub.setdefault("contract", max(SUPPORTED_CONTRACTS))
    hub.setdefault("mode", "local")
    hub.setdefault("url", None)
    hub.setdefault("published", {})
    hub.setdefault("removed", [])
    for r in removes:
        if r and r not in hub["removed"]:
            hub["removed"].append(r)
    hub["removed"] = [r for r in hub["removed"] if r not in restores]

    report = {"root": root, "ok": [], "needs_upgrade": [], "too_new": [], "broken": [],
              "removed": list(hub["removed"])}
    guides, current = [], {}
    for name in sorted(os.listdir(root)):
        folder = os.path.join(root, name)
        if not os.path.isfile(os.path.join(folder, "index.html")) or name.startswith((".", "_")):
            continue
        if name in hub["removed"]:
            continue
        status, meta, reasons = read_guide(folder)
        entry = {"slug": name, "reasons": reasons}
        if meta and meta.get("title"):
            entry["title"] = meta["title"]
        report[status].append(entry)
        if status != "ok":
            continue
        guides.append(card_fields(meta))
        for dirpath, _, files in os.walk(folder):
            for fn in files:
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                current[rel] = sha(p)

    if "--mark-published" in flags:
        hub["published"] = current
        hub["mode"] = "artifact" if hub.get("url") else hub["mode"]
        with open(hub_path, "w", encoding="utf-8") as f:
            json.dump(hub, f, ensure_ascii=False, indent=2)
        print(json.dumps({"marked": len(current)}))
        return 0

    s = dict(STRINGS.get(lang, STRINGS["en"]))
    if lang not in STRINGS:
        s["lang"] = lang
        report["note"] = f"no built-in strings for '{lang}'; pass --strings with translations of the English keys"
    if strings_file:
        with open(strings_file, encoding="utf-8") as f:
            s.update(json.load(f))

    guides.sort(key=lambda g: g.get("updated", ""), reverse=True)
    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    manifest = json.dumps({"strings": s, "guides": guides}, ensure_ascii=False)
    manifest = manifest.replace("</", "<\\/")
    page = page.replace("/*__HUB_MANIFEST__*/{}", manifest)
    page = page.replace('lang="__LANG__"', f'lang="{s["lang"]}"')
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

    # Supporting-file diff for the Artifact publish.
    published = hub.get("published", {})
    files = {rel: os.path.normpath(os.path.join(root, rel)) for rel, h in current.items()
             if published.get(rel) != h}
    for rel in published:
        if rel not in current:
            files[rel] = None
    report["files"] = files
    report["guide_count"] = len(guides)
    report["hub_page"] = os.path.join(root, "index.html")
    report["hub"] = {k: hub[k] for k in ("url", "mode", "contract")}
    report["image_warning"] = any(g["has_images"] for g in guides)

    with open(hub_path, "w", encoding="utf-8") as f:
        json.dump(hub, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
