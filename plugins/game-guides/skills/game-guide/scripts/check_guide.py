#!/usr/bin/env python3
"""Check a game guide against output contract v1 (references/output-contract.md).

Usage:
  python check_guide.py game-guides/<slug>            # folder holding index.html
  python check_guide.py game-guides/<slug>/index.html
  python check_guide.py game-guides/<slug> --meta     # print guide-meta JSON only

Exit code 0 = no errors (warnings allowed), 1 = errors, 2 = usage problem.
Standard library only.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

CONTRACT = 1
REQUIRED = {
    "contract": int,
    "slug": str,
    "game": str,
    "variant": str,
    "title": str,
    "lang": str,
    "summary": str,
    "game_version": str,
    "updated": str,
    "spoiler_gate": bool,
    "sources": list,
}
OPTIONAL = {
    "created": str,
    "platform": str,
    "dlc": (list, str),
    "player_profile": dict,
    "image_credits": list,
    "disputed": list,
    "artifact": dict,
}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:--[a-z0-9]+(?:-[a-z0-9]+)*)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")
RASTER = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif")
SIZE_WARN = 10 * 1024 * 1024

# Attributes that make the browser load something. <a href> is a link the reader
# clicks, not a load, so it is exempt from the external/relative rules.
LOAD_ATTRS = {
    "img": ("src", "srcset"),
    "script": ("src",),
    "iframe": ("src",),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
    "audio": ("src",),
    "image": ("href", "xlink:href"),
    "use": ("href", "xlink:href"),
    "link": ("href",),
}


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.has_charset = False
        self.has_viewport = False
        self.meta_blocks = []
        self.loads = []  # (tag, attr, value)
        self._in_meta = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "meta":
            if "charset" in a:
                self.has_charset = True
            if (a.get("name") or "").lower() == "viewport":
                self.has_viewport = True
        elif tag == "script" and a.get("id") == "guide-meta":
            self._in_meta = True
            self._buf = []
        for attr in LOAD_ATTRS.get(tag, ()):
            val = a.get(attr)
            if not val:
                continue
            if tag == "link":
                rel = (a.get("rel") or "").lower()
                if not any(r in rel for r in ("stylesheet", "icon", "preload", "modulepreload", "manifest")):
                    continue  # preconnect / dns-prefetch load nothing themselves
            if attr == "srcset" or (tag == "source" and attr == "srcset"):
                for part in val.split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.loads.append((tag, attr, url))
            else:
                self.loads.append((tag, attr, val))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_meta:
            self.meta_blocks.append("".join(self._buf))
            self._in_meta = False

    def handle_data(self, data):
        if self._in_meta:
            self._buf.append(data)


def check(path):
    errors, warnings = [], []
    if os.path.isdir(path):
        folder, index = path, os.path.join(path, "index.html")
    else:
        folder, index = os.path.dirname(path) or ".", path
    if not os.path.isfile(index):
        return None, [f"no index.html at {index}"], []

    with open(index, encoding="utf-8") as f:
        src = f.read()

    if not re.match(r"\s*<!doctype html>", src, re.I):
        errors.append("page does not start with <!doctype html> (fragment, not a full document)")

    scan = Scan()
    scan.feed(src)

    if not scan.html_lang:
        errors.append("<html lang> missing")
    if not scan.has_charset:
        errors.append("<meta charset> missing")
    if not scan.has_viewport:
        errors.append('<meta name="viewport"> missing')

    meta = None
    if len(scan.meta_blocks) == 0:
        errors.append('no <script type="application/json" id="guide-meta"> block')
    elif len(scan.meta_blocks) > 1:
        errors.append(f"{len(scan.meta_blocks)} guide-meta blocks; exactly one allowed")
    if scan.meta_blocks:
        try:
            meta = json.loads(scan.meta_blocks[0])
        except json.JSONDecodeError as e:
            errors.append(f"guide-meta is not valid JSON: {e}")

    if isinstance(meta, dict):
        for key, typ in REQUIRED.items():
            if key not in meta:
                errors.append(f"guide-meta.{key} missing (required)")
            elif typ is int and (isinstance(meta[key], bool) or not isinstance(meta[key], int)):
                errors.append(f"guide-meta.{key} must be an integer")
            elif not isinstance(meta[key], typ):
                errors.append(f"guide-meta.{key} must be {typ.__name__}")
            elif typ is str and not meta[key].strip():
                errors.append(f"guide-meta.{key} is empty")
        for key, typ in OPTIONAL.items():
            if key in meta and not isinstance(meta[key], typ):
                errors.append(f"guide-meta.{key} has the wrong type")
        if meta.get("contract") not in (None, CONTRACT) and isinstance(meta.get("contract"), int):
            errors.append(f"guide-meta.contract is {meta['contract']}; this checker knows {CONTRACT}")
        slug = meta.get("slug") if isinstance(meta.get("slug"), str) else None
        if slug and not SLUG_RE.match(slug):
            errors.append(f"slug '{slug}' must be lowercase a-z0-9 with '-' (variants add '--suffix')")
        if slug and os.path.isdir(path) and os.path.basename(os.path.normpath(folder)) != slug:
            errors.append(f"slug '{slug}' does not match folder name '{os.path.basename(os.path.normpath(folder))}'")
        game = meta.get("game") if isinstance(meta.get("game"), str) else None
        if game and not SLUG_RE.match(game):
            errors.append(f"game '{game}' must be a slug")
        if slug and game and not (slug == game or slug.startswith(game + "--")):
            warnings.append(f"slug '{slug}' is not '{game}' or '{game}--…'; check the variant naming")
        for key in ("updated", "created"):
            if isinstance(meta.get(key), str) and not DATE_RE.match(meta[key]):
                errors.append(f"guide-meta.{key} must be YYYY-MM-DD")
        if isinstance(meta.get("lang"), str) and scan.html_lang and meta["lang"] != scan.html_lang:
            errors.append(f"guide-meta.lang '{meta['lang']}' differs from <html lang='{scan.html_lang}'>")
        for i, s in enumerate(meta.get("sources") or []):
            if not isinstance(s, dict) or not s.get("name"):
                errors.append(f"guide-meta.sources[{i}] needs at least a name")
        if isinstance(meta.get("sources"), list) and not meta["sources"]:
            warnings.append("guide-meta.sources is empty")

    if re.search(r"data:image/", src, re.I):
        n = len(re.findall(r"data:image/", src, re.I))
        errors.append(f"{n} base64/data-URI image(s) embedded; move them to files under images/")

    # Asset loads from markup.
    for tag, attr, val in scan.loads:
        v = val.strip()
        if v.startswith("#") or v.startswith("data:"):
            continue
        if re.match(r"^(https?:)?//", v, re.I):
            host = re.sub(r"^(https?:)?//", "", v, flags=re.I).split("/")[0].lower()
            if host not in FONT_HOSTS:
                errors.append(f"<{tag} {attr}> loads external {v}")
            continue
        if re.match(r"^[a-z][a-z0-9+.-]*:", v, re.I):
            continue  # blob:, about:, etc.
        if v.startswith("/"):
            errors.append(f"<{tag} {attr}> uses an absolute path {v}; make it relative")
            continue
        rel = v.split("#")[0].split("?")[0]
        if rel and not os.path.isfile(os.path.join(folder, rel)):
            errors.append(f"<{tag} {attr}> points at {rel}, which does not exist in the guide folder")

    # CSS url()/@import.
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)|@import\s+['\"]([^'\"]+)['\"]", src):
        v = (m.group(1) or m.group(2) or "").strip()
        if not v or v.startswith("#") or v.startswith("data:"):
            continue
        if re.match(r"^(https?:)?//", v, re.I):
            host = re.sub(r"^(https?:)?//", "", v, flags=re.I).split("/")[0].lower()
            if host not in FONT_HOSTS:
                errors.append(f"CSS loads external {v}")
        elif not v.startswith("/") and not os.path.isfile(os.path.join(folder, v.split("?")[0])):
            errors.append(f"CSS url({v}) does not exist in the guide folder")

    # localStorage keys.
    slug = meta.get("slug") if isinstance(meta, dict) and isinstance(meta.get("slug"), str) else None
    # Simple string constants (var KEY = 'x') so KEY resolves to its value.
    consts = dict(re.findall(r"\b(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*['\"]([^'\"]*)['\"]", src))
    seen = set()
    # Keys taken from data-key attributes (the checklist component): check the attributes themselves.
    for var in re.findall(r"\b(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*\w+\.getAttribute\(\s*['\"]data-key['\"]\s*\)", src):
        seen.add(var)
    for key in re.findall(r'data-key="([^"]*)"', src):
        if slug and not key.startswith(slug + ":"):
            errors.append(f"data-key '{key}' must start with '{slug}:'")
    for m in re.finditer(r"localStorage\s*\.\s*(setItem|getItem|removeItem)\s*\(\s*([^,)]*)", src):
        op, arg = m.group(1), m.group(2).strip()
        lit = re.match(r"^(['\"`])(.*?)\1$", arg)
        key = lit.group(2) if lit and "${" not in lit.group(2) else consts.get(arg)
        if key is None:
            if arg not in seen:
                warnings.append(f"localStorage key built from '{arg}' — confirm it starts with the slug")
                seen.add(arg)
            continue
        if slug and not key.startswith(slug + ":"):
            if op == "setItem":
                errors.append(f"localStorage key '{key}' must start with '{slug}:'")
            elif (op, key) not in seen:
                warnings.append(f"localStorage {op}('{key}') reads an un-prefixed key — fine only for migrating old saves")
                seen.add((op, key))
    if re.search(r"localStorage\s*\[", src):
        warnings.append("localStorage used with [] indexing — confirm keys start with the slug")

    # Narrow-screen overflow: a `1fr` grid column grows to its widest child.
    if re.search(r"grid-template-columns\s*:\s*1fr\s*[;}]", src) and not re.search(
            r"(main|>\s*\*)\s*\{[^}]*min-width\s*:\s*0", src):
        warnings.append("a grid uses `grid-template-columns:1fr` without `min-width:0` on its children — "
                        "wide tables will make the page scroll sideways on phones; use minmax(0,1fr)")

    # Host-specific wording (common phrasings; not exhaustive).
    for phrase in ("private page", "หน้าส่วนตัว", "tell claude", "บอกได้ เดี๋ยวแก้"):
        if phrase.lower() in src.lower():
            warnings.append(f"wording '{phrase}' assumes where the page lives")

    # Folder-level checks.
    total, rasters = 0, []
    for root, _, files in os.walk(folder):
        for name in files:
            p = os.path.join(root, name)
            total += os.path.getsize(p)
            if name.lower().endswith(RASTER):
                rasters.append(os.path.relpath(p, folder))
    if rasters and isinstance(meta, dict) and not meta.get("image_credits"):
        warnings.append(f"{len(rasters)} raster image(s) ship with the guide but image_credits is empty")
    if total > SIZE_WARN:
        warnings.append(f"guide folder is {total / 1048576:.1f} MB (> 10 MB); an Artifact page tops out at 16 MB")

    return meta, errors, warnings


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    meta, errors, warnings = check(args[0])
    if "--meta" in argv:
        if meta is None:
            for e in errors:
                print("ERROR", e, file=sys.stderr)
            return 1
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0 if not errors else 1
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
