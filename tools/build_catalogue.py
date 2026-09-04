#!/usr/bin/env python3
"""Régénère `catalogue.json` à partir du contenu réel de `vendors/` et `icons/`.

    python3 tools/build_catalogue.py            # écrit catalogue.json
    python3 tools/build_catalogue.py --check    # ne rien écrire, sortir 1 si obsolète

Le catalogue **n'est pas maintenu à la main** : il est dérivé des fichiers présents. Un
logo ajouté dans `vendors/` apparaît au prochain passage ; un logo retiré disparaît. La
seule chose qui ne se déduit pas du binaire — d'où vient le fichier — vit dans les deux
relevés de provenance versionnés à côté des assets :

* `vendors/_sources.json` — repris tel quel du cowork Flowmetrik (`assets/tools/fetch_vendors.py`).
* `icons/_sources.md` — la correspondance `<slug>.svg ← <NomIcone>` du paquet Hugeicons.

Un asset sans provenance connue reste dans le catalogue, avec `source: null` : mieux vaut
un trou visible qu'une URL inventée.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "catalogue.json"
GABARIT = ROOT / "tools" / "index_template.html"
INDEX = ROOT / "docs" / "index.html"
MARQUES = ROOT / "MARQUES.md"
MARQUE_GABARIT = "/*__CATALOGUE__*/"
DEBUT = "<!-- TABLE:DEBUT — généré par tools/build_catalogue.py, ne pas éditer à la main -->"
FIN = "<!-- TABLE:FIN -->"

EXTENSIONS = {".svg": "svg", ".png": "png", ".jpg": "jpg", ".jpeg": "jpg"}

LICENCE_VENDOR = "marque déposée de son propriétaire — usage nominatif d'identification"
LICENCES_ICON = {
    "hugeicons": "Hugeicons free (MIT) — @hugeicons/core-free-icons, style stroke-rounded",
    "lucide": "Lucide (ISC), servie par api.iconify.design — trait ramené à 1.5 pour "
              "cohabiter avec les Hugeicons",
    None: "icône libre — famille non tracée, voir icons/_sources.md",
}
PREFIXES_ICON = {
    "hugeicons": "@hugeicons/core-free-icons#",
    "lucide": "lucide#",
}

NOTE_VENDOR = (
    "Redistribué pour identifier l'outil dans un document. Flowmetrik ne revendique "
    "aucun droit sur cette marque et n'est ni affilié ni sponsorisé par son propriétaire. "
    "Voir MARQUES.md."
)
NOTE_ICON = "Icône libre, recolorable — `stroke=\"currentColor\"`, la couleur vient du CSS."

# Les couleurs qu'on ne retient jamais comme « couleur de marque » : elles décrivent
# le fond ou le trait, pas l'identité.
NEUTRES = {"#000000", "#ffffff", "#fff", "#000", "none", "currentcolor", "transparent"}

RE_HEX = re.compile(r"(?:fill|stop-color|stroke)\s*[:=]\s*[\"']?(#[0-9a-fA-F]{3,8})", re.I)


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def _hex6(valeur: str) -> str | None:
    """Normalise en #rrggbb ; rend None pour ce qui n'est pas une couleur exploitable."""
    v = valeur.strip().lower()
    if len(v) == 4:  # #abc
        v = "#" + "".join(c * 2 for c in v[1:])
    if len(v) == 9:  # #rrggbbaa — on jette l'alpha
        v = v[:7]
    return v if re.fullmatch(r"#[0-9a-f]{6}", v) else None


def couleur_marque(chemin: pathlib.Path) -> str | None:
    """La teinte dominante déclarée dans le SVG, ou None.

    On compte les occurrences plutôt que de prendre la première : un logo commence
    souvent par un fond blanc ou un masque noir, qui ne sont pas sa couleur.
    Rien pour un PNG : une couleur moyennée sur des pixels serait une invention.
    """
    if chemin.suffix.lower() != ".svg":
        return None
    try:
        texte = chemin.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    compte: collections.Counter[str] = collections.Counter()
    for brut in RE_HEX.findall(texte):
        h = _hex6(brut)
        if h and h not in NEUTRES:
            compte[h] += 1
    if not compte:
        return None
    return compte.most_common(1)[0][0]


def nom_lisible(slug: str) -> str:
    """`feuille-de-route` → « Feuille de route ». Repli quand aucune source ne nomme l'asset."""
    mots = slug.replace("_", "-").split("-")
    return " ".join([mots[0].capitalize(), *mots[1:]])


def provenance_vendors() -> dict[str, dict]:
    fichier = ROOT / "vendors" / "_sources.json"
    if not fichier.exists():
        return {}
    return {e["file"]: e for e in json.loads(fichier.read_text(encoding="utf-8")) if e.get("file")}


def provenance_icons(presents: set[str]) -> dict[str, tuple[str | None, str]]:
    """Rend `{fichier: (nom d'origine ou None, famille)}` d'après `icons/_sources.md`.

    Deux familles cohabitent et n'ont pas la même licence : **Hugeicons** (MIT) pour la
    majorité, **Lucide** (ISC) pour les vingt icônes FlowGov et les huit `agent-*`.

    Le relevé les note de deux façons — une puce `- \\`x.svg\\` ← NomIcone`, ou une simple
    énumération de slugs entre accents graves. La seconde forme est ambiguë : une section
    contient aussi des noms de scripts et des URLs entre accents graves. D'où le filtre
    `presents` — un slug n'est retenu que s'il correspond à un fichier réellement là.
    """
    fichier = ROOT / "icons" / "_sources.md"
    if not fichier.exists():
        return {}
    texte = fichier.read_text(encoding="utf-8")
    puce = re.compile(r"`([\w\-]+\.svg)`\s*(?:←|<-)\s*`?([A-Za-z0-9_\-]+)`?")
    inline = re.compile(r"`([\w\-]+)`")

    provenance: dict[str, tuple[str | None, str]] = {}
    for bloc in re.split(r"^##\s", texte, flags=re.M):
        famille = "lucide" if "lucide" in bloc.lower() else "hugeicons"
        explicites = set()
        for m in puce.finditer(bloc):
            provenance[m.group(1)] = (m.group(2), famille)
            explicites.add(m.group(1))
        for m in inline.finditer(bloc):
            nom = f"{m.group(1)}.svg"
            if nom in presents and nom not in explicites and nom not in provenance:
                provenance[nom] = (None, famille)
    return provenance


def collecte(dossier: str, type_: str, vendors: dict, icons: dict) -> list[dict]:
    base = ROOT / dossier
    entrees = []
    for chemin in sorted(base.iterdir()):
        if not chemin.is_file() or chemin.name.startswith("_") or chemin.name.startswith("."):
            continue
        fmt = EXTENSIONS.get(chemin.suffix.lower())
        if fmt is None:
            continue
        slug = chemin.stem
        if type_ == "vendor":
            meta = vendors.get(chemin.name, {})
            nom = meta.get("marque") or nom_lisible(slug)
            source = meta.get("source")
            usage = meta.get("usage")
            licence, note = LICENCE_VENDOR, NOTE_VENDOR
        else:
            icone, famille = icons.get(chemin.name, (None, None))
            nom = nom_lisible(slug)
            # Famille connue mais nom d'origine non tracé : on rend la famille seule.
            # Reconstituer un nom d'icône par ressemblance serait une invention.
            source = (f"{PREFIXES_ICON[famille]}{icone}" if icone else famille) if famille else None
            usage = famille
            licence, note = LICENCES_ICON[famille], NOTE_ICON
        entrees.append({
            "slug": slug,
            "nom": nom,
            "fichier": f"{dossier}/{chemin.name}",
            "type": type_,
            "format": fmt,
            "taille": chemin.stat().st_size,
            "sha256": _sha256(chemin),
            "source": source,
            "releve": (vendors.get(chemin.name, {}) or {}).get("releve"),
            "usage": usage,
            "couleur_marque": couleur_marque(chemin),
            "licence": licence,
            "note": note,
        })
    return entrees


def construire() -> dict:
    presents = {p.name for p in (ROOT / "icons").iterdir()} if (ROOT / "icons").exists() else set()
    vendors, icons = provenance_vendors(), provenance_icons(presents)
    assets = collecte("vendors", "vendor", vendors, icons) + collecte("icons", "icon", vendors, icons)
    return {
        "schema": "flowmetrik.flowlogos/1.0",
        "depot": "https://github.com/flowmetrik/flowlogos",
        "genere_par": "tools/build_catalogue.py",
        "avertissement": (
            "Les logos d'éditeurs sont les marques de leurs propriétaires respectifs. "
            "Ils sont réunis ici pour les identifier, pas pour être exploités comme une "
            "marque de Flowmetrik. Lire MARQUES.md avant tout réemploi."
        ),
        "total": len(assets),
        "par_type": {
            "vendor": sum(1 for a in assets if a["type"] == "vendor"),
            "icon": sum(1 for a in assets if a["type"] == "icon"),
        },
        "sans_source": sorted(a["fichier"] for a in assets if not a["source"]),
        "assets": assets,
    }


def rendre_index(catalogue: dict) -> str:
    """Injecte le catalogue **dans** la page.

    La page ne va chercher aucun fichier au chargement : ni CDN, ni `fetch` du catalogue.
    Une page qui ferait `fetch("../catalogue.json")` s'afficherait vide en `file://` — la
    politique d'origine bloque la requête, et **rien ne le dit à l'écran**.
    """
    charge = json.dumps(catalogue, ensure_ascii=False, separators=(",", ":"))
    if "</script" in charge.lower():
        raise SystemExit("un champ du catalogue contient </script> — refus d'écrire la page")
    gabarit = GABARIT.read_text(encoding="utf-8")
    if MARQUE_GABARIT not in gabarit:
        raise SystemExit(f"marque {MARQUE_GABARIT} absente de {GABARIT.name}")
    return gabarit.replace(MARQUE_GABARIT, charge)


def rendre_marques(catalogue: dict) -> str:
    """Réécrit la table des marques de MARQUES.md entre ses deux balises.

    Le texte juridique est écrit à la main et ne bouge pas ; seule la liste des marques est
    dérivée du contenu de `vendors/`. Une liste tenue à la main finit toujours par citer une
    marque qui n'est plus là, ou par en taire une qui vient d'arriver.
    """
    lignes = [
        DEBUT,
        "",
        f"## Les {catalogue['par_type']['vendor']} marques présentes dans `vendors/`",
        "",
        "| Marque | Fichier | Provenance du fichier |",
        "|---|---|---|",
    ]
    for a in catalogue["assets"]:
        if a["type"] != "vendor":
            continue
        source = a["source"] or "_non tracée_"
        if source.startswith("http"):
            source = f"[{source.split('//')[1][:52]}]({source})"
        lignes.append(f"| {a['nom']} | `{a['fichier']}` | {source} |")
    lignes += ["", FIN]
    table = "\n".join(lignes)

    texte = MARQUES.read_text(encoding="utf-8")
    if DEBUT not in texte or FIN not in texte:
        raise SystemExit("balises TABLE:DEBUT / TABLE:FIN absentes de MARQUES.md")
    avant = texte.split(DEBUT)[0]
    apres = texte.split(FIN, 1)[1]
    return avant + table + apres


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="ne rien écrire ; sortir 1 si le catalogue versionné est périmé")
    args = ap.parse_args()

    catalogue = construire()
    rendu = json.dumps(catalogue, ensure_ascii=False, indent=1) + "\n"
    page = rendre_index(catalogue)
    marques = rendre_marques(catalogue)

    if args.check:
        actuel = CATALOGUE.read_text(encoding="utf-8") if CATALOGUE.exists() else ""
        page_actuelle = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        if actuel != rendu or page_actuelle != page \
                or MARQUES.read_text(encoding="utf-8") != marques:
            print("catalogue.json, docs/index.html ou MARQUES.md est périmé "
                  "— relancer sans --check")
            return 1
        print(f"catalogue.json, docs/index.html et MARQUES.md à jour "
              f"— {catalogue['total']} assets")
        return 0

    CATALOGUE.write_text(rendu, encoding="utf-8")
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(page, encoding="utf-8")
    MARQUES.write_text(marques, encoding="utf-8")
    p = catalogue["par_type"]
    print(f"catalogue.json + docs/index.html + MARQUES.md — {catalogue['total']} assets "
          f"({p['vendor']} logos, {p['icon']} icônes)")
    if catalogue["sans_source"]:
        print(f"  {len(catalogue['sans_source'])} sans provenance connue :")
        for f in catalogue["sans_source"]:
            print(f"    {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
