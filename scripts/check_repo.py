#!/usr/bin/env python3
"""Comprueba perfiles, traducción y enlaces locales sin acceder a la red."""

import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from firelibre import core  # noqa: E402


def main():
    protected = core.protected_packages()
    for name in core.PROFILES:
        rules = core.profile(name)
        ids = [p["id"] for p in rules["packages"]]
        assert len(ids) == len(set(ids)), "Paquetes repetidos"
        assert not set(ids) & protected, "El perfil incluye paquetes protegidos"
        assert all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_.]+", pkg) for pkg in ids)
    folders = ROOT / "integrations/dumbtv/res"
    default = {s.attrib["name"] for s in ET.parse(folders / "values/strings.xml").getroot()}
    spanish = {s.attrib["name"] for s in ET.parse(folders / "values-es/strings.xml").getroot()}
    assert default == spanish, "Faltan traducciones"
    for path in [ROOT / "README.md", *ROOT.glob("docs/*.md"), *ROOT.glob("prompts/*.md"), *ROOT.glob("*.md")]:
        if not path.exists():
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            filename = target.split("#")[0]
            assert (path.parent / filename).exists(), f"Enlace roto en {path.name}: {target}"
    for path in ROOT.rglob("*.json"):
        if not any(part in {"state", "work", ".git"} for part in path.relative_to(ROOT).parts):
            json.loads(path.read_text(encoding="utf-8"))
    print(f"Perfiles, enlaces y {len(spanish)} recursos traducidos: correctos.")


if __name__ == "__main__":
    main()
