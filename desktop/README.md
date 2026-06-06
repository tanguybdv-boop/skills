# 💼 Comptabilité Pro — Logiciel de bureau

Application de bureau (Windows / macOS / Linux) pour la comptabilité d'autoentrepreneur :
factures clients/fournisseurs, URSSAF, TVA, déclarations. Construite avec **Electron**
en réutilisant l'interface HTML/JS, avec stockage **local** (aucun serveur, aucune donnée envoyée).

## 📦 Contenu

```
desktop/
├── main.js          # Processus principal Electron (fenêtre, menu, cycle de vie)
├── preload.js       # Pont sécurisé (contextIsolation)
├── package.json     # Dépendances + configuration de build (electron-builder)
├── web/             # L'interface (portail + comptabilité)
│   ├── comptabilite_client_portail.html
│   └── comptabilite_autoentrepreneur.html
└── assets/          # Icône de l'application
```

## 🚀 Lancer en développement

Prérequis : **Node.js 18+** installé.

```bash
cd desktop
npm install      # installe Electron (~1re fois, ~100 Mo)
npm start        # lance l'application
```

La fenêtre s'ouvre sur le **portail de connexion**. Crée un compte, connecte-toi,
puis accède à la **comptabilité complète** (menu *Fichier → Comptabilité complète*,
ou le bouton dans le tableau de bord).

## 🏗️ Générer un installateur (logiciel distribuable)

`electron-builder` produit de vrais installateurs natifs.

```bash
# Pour votre OS courant
npm run dist

# Cibles spécifiques
npm run dist:win     # Windows : .exe (installateur NSIS) + version portable
npm run dist:mac     # macOS   : .dmg
npm run dist:linux   # Linux   : .AppImage + .deb
```

Les fichiers générés apparaissent dans `desktop/dist/`.

> Note : pour construire un `.exe` Windows il faut généralement être sous Windows
> (ou utiliser un runner Windows en CI). De même le `.dmg` se construit sous macOS.
> Le `.AppImage`/`.deb` Linux se construit sous Linux.

## ⌨️ Raccourcis

| Raccourci | Action |
|-----------|--------|
| `Ctrl/Cmd + H` | Revenir au portail (accueil) |
| `Ctrl/Cmd + K` | Ouvrir la comptabilité complète |
| `Ctrl/Cmd + R` | Recharger |
| `Ctrl/Cmd + +/-` | Zoom |
| `F11` | Plein écran |

## 💾 Données

- Stockées **localement** via `localStorage` (par machine, par utilisateur OS).
- Aucune connexion réseau, aucune donnée transmise.
- Sauvegarde/export disponibles depuis le portail (modèle CSV, backup JSON).

## 🔧 Détails techniques

- **Sécurité** : `contextIsolation: true`, `nodeIntegration: false`.
- **Navigation** : les liens entre pages locales fonctionnent ; les liens
  `http(s)` s'ouvrent dans le navigateur système.
- **Icône** : remplace `assets/icon.png` par ton propre logo (512×512 recommandé,
  `.png` ; electron-builder génère les formats `.ico`/`.icns` automatiquement).

## 🖼️ Capture d'écran (outil de dev)

`_screenshot.js` permet de générer des PNG de l'interface en headless :

```bash
xvfb-run -a ./node_modules/.bin/electron --no-sandbox _screenshot.js \
  web/comptabilite_autoentrepreneur.html sortie.png [injection.js]
```

(Outil interne ; non inclus dans l'application packagée.)
