#!/usr/bin/env python3
"""Génère index.xml pour ReaPack.

Usage :  python3 build_index.py COMPTE_GITHUB NOM_DU_DEPOT [branche]
Exemple : python3 build_index.py nicolasdebois heaj-voice-spectral main

À relancer (après avoir augmenté la version dans l'en-tête des fichiers) à chaque mise à jour,
puis commit + push de index.xml.
"""
import re, sys, datetime, pathlib
from xml.sax.saxutils import escape, quoteattr

user = sys.argv[1] if len(sys.argv) > 1 else "VOTRE-COMPTE"
repo = sys.argv[2] if len(sys.argv) > 2 else "heaj-voice-spectral"
branch = sys.argv[3] if len(sys.argv) > 3 else "main"
root = pathlib.Path(__file__).parent
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PACKAGES = [
    ("Effects/HEAJ/heaj_voice_spectral", "effect",
     "HEAJ Voice Spectral : compression spectrale + déesseur, trois curseurs et analyse automatique (effet JS)"),
]

def header(text, key):
    m = re.search(r"(?:@|^)%s:?[ \t]*(\S.*)" % key, text, re.M)
    return m.group(1).strip() if m else ""

out = ['<?xml version="1.0" encoding="utf-8"?>', '<index version="1" name="HEAJ Voice Spectral">',
       '  <category name="HEAJ">']
for path, typ, desc in PACKAGES:
    text = (root / path).read_text(encoding="utf-8")
    version = header(text, "version") or "0.0.1"
    author = header(text, "author") or "HEAJ"
    url = f"https://github.com/{user}/{repo}/raw/{branch}/{path}"
    name = path.split("/")[-1]
    attrs = ' main="main"' if typ == "script" else ""
    out += [f'    <reapack name={quoteattr(name)} type="{typ}" desc={quoteattr(desc)}>',
            f'      <version name={quoteattr(version)} author={quoteattr(author)} time="{now}">',
            f'        <source{attrs}>{escape(url)}</source>',
            '      </version>', '    </reapack>']
out += ['  </category>', '</index>', '']
(root / "index.xml").write_text("\n".join(out), encoding="utf-8")
print("index.xml écrit pour", f"{user}/{repo}@{branch}")
