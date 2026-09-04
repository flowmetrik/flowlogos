# Icônes

Hugeicons, paquet libre `@hugeicons/core-free-icons` v4.2.3, style `stroke-rounded`.
Converties en SVG inline par `commercial/diags-bpifrance/build_icons.py`.
`stroke="currentColor"` : la couleur vient du CSS, jamais du fichier.

- `duree.svg` ← Calendar03Icon
- `montant.svg` ← Invoice01Icon
- `subvention.svg` ← PercentCircleIcon
- `reste-a-charge.svg` ← Wallet01Icon
- `etat-des-lieux.svg` ← SearchVisualIcon
- `cas-usage.svg` ← BulbIcon
- `feuille-de-route.svg` ← RoadLocation01Icon
- `rapport.svg` ← DocumentValidationIcon
- `representant-legal.svg` ← UserCheck01Icon
- `comptable.svg` ← CalculatorIcon
- `direction.svg` ← PresentationBarChart01Icon
- `equipes.svg` ← UserGroupIcon

## Recrutement

Ajoutées par `recrutement/tools/build_icons.py`.

- `telephone.svg` ← Call02Icon
- `code.svg` ← SourceCodeIcon
- `entraide.svg` ← HandshakeIcon
- `performance.svg` ← Target01Icon
- `ia.svg` ← AiBrain01Icon
- `lieu.svg` ← Location01Icon
- `contrat.svg` ← Briefcase01Icon
- `demarrage.svg` ← Rocket01Icon
- `prospection.svg` ← Megaphone01Icon
- `donnees.svg` ← Database01Icon
- `verification.svg` ← CheckmarkBadge01Icon
- `candidature.svg` ← Mail01Icon
- `utilisateur.svg` ← UserGroupIcon
- `outil-agentique.svg` ← ComputerTerminal01Icon
- `connecteurs.svg` ← PlugSocketIcon
- `systeme-information.svg` ← ServerStack01Icon

## Ajout du 2026-08-20 — FlowGov

Vingt icônes manquantes pour le kit d'intégration FlowGov, tirées de **Lucide** via l'API
Iconify (ouverte, sans clé) — le MCP Hugeicons n'est pas authentifiable en session détachée.
Le trait a été ramené de 2 à **1.5** pour s'aligner sur le style `stroke-rounded` des
Hugeicons déjà présentes ; sans cet ajustement, les deux familles ne cohabitent pas.

`email` · `calendrier` · `verrou` · `institution` · `apprendre` · `canal` · `cible` ·
`salon` · `seuil` · `conformite` · `question` · `recherche` · `croissance` · `batiment` ·
`procedure` · `service-fait` · `appel` · `decideurs` · `parcours` · `arbitrage`

Vérifier l'existence d'un nom Lucide avant de tirer — un nom inventé renvoie 404 et fait
tomber toute la passe : `https://api.iconify.design/lucide.json?icons=<nom>`.
Piège rencontré : `help-circle` et `circle-help` n'existent pas, le nom est
`circle-question-mark`.

## FlowSkills

Ajoutées le 2026-09-03 pour la carte des entités et l'arborescence — `flowskills/build_icones.py`.

- `applications.svg` ← Grid2X2Icon
- `arborescence.svg` ← Structure01Icon
- `cle.svg` ← Key01Icon
- `design.svg` ← PaintBoardIcon
- `dossier.svg` ← Folder01Icon
- `formation.svg` ← Mortarboard02Icon
- `lien-casse.svg` ← LinkBackwardIcon
- `machine.svg` ← ServerStack01Icon
- `pilotage.svg` ← DashboardSquare01Icon
- `produit.svg` ← PuzzleIcon
- `savoir.svg` ← Book02Icon

## Schéma « agent IA » — Lucide

Les huit `agent-*.svg` viennent de **Lucide**, importées par
`recrutement/tools/import_icones_site.py` (trait ramené à 1.55 pour cohabiter avec les
Hugeicons). Elles n'étaient tracées que dans le code : sans cette section, le catalogue
public `flowmetrik/flowlogos` les rendait sans provenance.

- `agent-cerveau.svg` ← brain-circuit
- `agent-fichiers.svg` ← file-stack
- `agent-internet.svg` ← globe-2
- `agent-mcp.svg` ← plug
- `agent-memoire.svg` ← memory-stick
- `agent-skills.svg` ← book-open-check
- `agent-sortie.svg` ← circle-check-big
- `agent-utilisateur.svg` ← user-round
