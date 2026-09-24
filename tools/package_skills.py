#!/usr/bin/env python3
"""Zip every skill for claude.ai upload: dist/<skill>.zip, each holding <skill>/SKILL.md etc.

Usage: python tools/package_skills.py
Attach the zips to a GitHub release (gh release create vX.Y.Z dist/*.zip).
"""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SKIP_DIRS = {"__pycache__", "evals"}


def main():
    os.makedirs(DIST, exist_ok=True)
    plugins = os.path.join(ROOT, "plugins")
    made = []
    for plugin in sorted(os.listdir(plugins)):
        skills = os.path.join(plugins, plugin, "skills")
        if not os.path.isdir(skills):
            continue
        for skill in sorted(os.listdir(skills)):
            src = os.path.join(skills, skill)
            if not os.path.isfile(os.path.join(src, "SKILL.md")):
                continue
            out = os.path.join(DIST, f"{skill}.zip")
            with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
                for dirpath, dirnames, files in os.walk(src):
                    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                    for fn in files:
                        if fn.endswith(".pyc"):
                            continue
                        p = os.path.join(dirpath, fn)
                        z.write(p, os.path.join(skill, os.path.relpath(p, src)))
            made.append(out)
    for m in made:
        print(m)


if __name__ == "__main__":
    main()
