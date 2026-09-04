# flowlogos

> Le catalogue documenté des **assets globaux** de Flowmetrik : logos d'éditeurs et icônes,
> servis comme une bibliothèque réutilisable, chacun avec sa provenance et son empreinte.

**Catalogue en ligne → <https://flowmetrik.github.io/flowlogos/docs/>**

Un document Flowmetrik — plaquette, deck, page web, schéma d'architecture — nomme des
outils. Jusqu'ici, chaque projet allait rechercher le même logo Slack, la même icône
« données », et repartait avec un fichier légèrement différent, sans provenance et sans date.
Ce dépôt met fin à cette dispersion : **un asset, un endroit, une source connue**.

Il ne contient que ce qui est **global** : rien de spécifique à un client, rien qui engage
une relation commerciale.

## Ce qu'il y a dedans

| Dossier | Contenu | Licence |
|---|---|---|
| `vendors/` | logos d'éditeurs et d'outils, dans leur teinte de marque | marques de leurs propriétaires — voir [`MARQUES.md`](MARQUES.md) |
| `icons/` | icônes d'interface, `stroke="currentColor"` donc recolorables | Hugeicons free (MIT) et Lucide (ISC) |
| `catalogue.json` | l'index machine de tout ce qui précède | — |
| `docs/index.html` | la grille cherchable, publiée par GitHub Pages | — |
| `tools/` | le générateur du catalogue et de la page | libre |

Chaque entrée de `catalogue.json` porte : `slug`, `nom`, `fichier`, `type`
(`vendor`\|`icon`), `format`, `taille`, `sha256`, `source`, `releve`, `usage`,
`couleur_marque` et le couple `licence` / `note`.

Le champ `sans_source`, en tête du catalogue, liste sans détour les fichiers dont la
provenance n'a pas pu être établie. **Un trou visible vaut mieux qu'une URL plausible** :
aucune source n'est devinée par ressemblance.

## S'en servir

### Par l'URL brute

```
https://raw.githubusercontent.com/flowmetrik/flowlogos/main/vendors/<slug>.svg
https://raw.githubusercontent.com/flowmetrik/flowlogos/main/icons/<nom>.svg
```

```html
<img src="https://raw.githubusercontent.com/flowmetrik/flowlogos/main/vendors/notion.svg"
     alt="Notion" height="28">
```

Sur la page du catalogue, **cliquer sur une vignette copie son URL brute**.

`raw.githubusercontent.com` sert du `text/plain` : un SVG y est parfait en `<img src>`,
mais ne s'ouvre pas comme une page dans un navigateur. Pour un document imprimé — plaquette,
PDF — télécharger le fichier et le poser en local : un rendu PDF ne doit jamais dépendre du
réseau au moment du build.

### Par le catalogue

```bash
curl -s https://raw.githubusercontent.com/flowmetrik/flowlogos/main/catalogue.json \
  | jq -r '.assets[] | select(.type=="vendor") | "\(.slug)\t\(.couleur_marque // "-")"'
```

`sha256` permet de vérifier qu'un fichier local est bien celui du catalogue, et de repérer
qu'un logo a changé sans qu'on l'ait décidé.

### Dans le cowork Flowmetrik

Les assets restent servis depuis `assets/library/` — ce dépôt en est la **publication**, pas
la source. Ne pas éditer un fichier ici en espérant qu'il redescende.

## Ajouter un logo

Tout part du cowork, jamais de ce dépôt.

1. **Récupérer le logo** avec l'outil prévu, qui écrit aussi sa provenance dans
   `assets/library/vendors/_sources.json` :

   ```bash
   # dans flowmetrik-cowork — ajouter une ligne à la liste OUTILS, puis :
   python3 assets/tools/fetch_vendors.py
   ```

   Simple Icons d'abord (SVG, CC0, teinte de marque), logo.dev en repli (PNG).
   **Regarder le fichier obtenu.** logo.dev résout par domaine : `teams.microsoft.com` et
   `powerbi.microsoft.com` rendent tous deux le favicon de `microsoft.com`, donc le logo
   Microsoft sous un autre nom — et rien dans la sortie ne le signale. Le repli, dans ce
   cas, est Wikimedia Commons.

2. **Recopier et régénérer**, sans rien committer :

   ```bash
   python3 assets/tools/push_flowlogos.py --apply
   ```

   Le script refuse de recopier un fichier dont le nom recoupe un slug client connu.

3. **Relire, puis publier** depuis ce clone :

   ```bash
   git add -A && git status
   git commit -m "vendors : <marque>" && git push
   ```

Un asset ajouté à la main dans ce dépôt sans passer par le cowork sera signalé comme
orphelin à la synchronisation suivante.

## Régénérer le catalogue

```bash
python3 tools/build_catalogue.py           # écrit catalogue.json, docs/index.html, MARQUES.md
python3 tools/build_catalogue.py --check   # sort 1 si l'un des trois est périmé
```

Le catalogue est **dérivé du contenu réel des dossiers** : il ne se maintient pas à la main.
La page `docs/index.html` embarque ses données — pas de CDN, pas de `fetch`, elle s'ouvre
aussi bien en `file://` qu'en ligne.

## Marques — à lire avant tout réemploi

Les logos de `vendors/` sont les **marques déposées de leurs propriétaires respectifs**.
Flowmetrik (BOOTLY SASU) n'en détient aucun droit, n'est affiliée à aucun de ces éditeurs, et
n'est ni sponsorisée ni approuvée par eux.

Ils sont réunis ici pour un **usage nominatif d'identification** : montrer le logo d'un outil
à côté de son nom, pour désigner cet outil. Toute reprise qui suggérerait un partenariat, une
certification ou une origine commune sort de ce cadre. Les règles de marque publiées par
chaque éditeur priment sur ce dépôt.

**Aucun logo de client de Flowmetrik ne figure ici, et aucun n'y figurera** : citer un client
suppose son accord écrit, ce qu'un dépôt public ne peut pas porter.

Détail, liste des marques et procédure de retrait : [`MARQUES.md`](MARQUES.md).
