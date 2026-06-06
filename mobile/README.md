# 📱 Comptabilité Pro — Application mobile

Version mobile de la plateforme comptable, sous deux formes :

1. **PWA** (Progressive Web App) — installable directement sur le téléphone
   (« Ajouter à l'écran d'accueil »), plein écran, **fonctionne hors-ligne**.
2. **APK Android natif** — via **Capacitor**, compilé en CI (GitHub Actions).

Les données restent **locales** sur le téléphone (localStorage). Aucun serveur.

## 📂 Structure

```
mobile/
├── www/                         # L'application web (PWA)
│   ├── index.html               # Entrée = portail (connexion/inscription + dashboard)
│   ├── comptabilite_autoentrepreneur.html
│   ├── manifest.webmanifest     # Manifest PWA (nom, icônes, couleurs, standalone)
│   ├── sw.js                    # Service worker (cache hors-ligne)
│   └── icons/                   # icon-192.png, icon-512.png
├── android/                     # Projet natif Android (généré par Capacitor)
├── capacitor.config.json        # appId fr.comptabilite.pro, webDir=www
└── package.json
```

## 🅰️ Option 1 — PWA (la plus rapide)

La PWA doit être servie en **HTTP(S)** (le service worker ne fonctionne pas en `file://`).

### En local
```bash
cd mobile
npm run serve        # sert www/ sur http://localhost:8099
```
Ouvre l'URL sur ton téléphone (même réseau Wi-Fi, via l'IP de l'ordinateur),
puis **menu navigateur → « Ajouter à l'écran d'accueil »**.

### En ligne (GitHub Pages)
Le workflow `.github/workflows/build-mobile.yml` publie automatiquement `www/`
sur **GitHub Pages**. Active Pages dans les *Settings* du dépôt
(*Build and deployment → Source : GitHub Actions*). L'URL publique est alors
installable sur n'importe quel téléphone.

> Sur iPhone : Safari → Partager → « Sur l'écran d'accueil ».
> Sur Android : Chrome propose « Installer l'application ».

## 🤖 Option 2 — APK Android natif (Capacitor)

### Compilation automatique (recommandé)
Le workflow GitHub Actions **`Build Mobile App`** compile l'APK à chaque push
qui touche `mobile/` (les runners GitHub ont accès au SDK Android). Récupère
l'APK dans l'onglet **Actions → run → Artifacts → `comptabilite-pro-apk`**.

> ⚠️ La compilation locale dans cet environnement n'est pas possible : l'accès
> aux serveurs Google (SDK Android, dépôt Maven) y est bloqué. La CI résout ce point.

### Compilation locale (sur ta machine)
Prérequis : **Node 18+**, **JDK 17/21**, **Android SDK** (Android Studio).
```bash
cd mobile
npm install
npx cap sync android
cd android
./gradlew assembleDebug      # APK debug
# → android/app/build/outputs/apk/debug/app-debug.apk
```
Ou ouvre le projet dans Android Studio :
```bash
npx cap open android
```

### Publier sur le Play Store
1. `./gradlew bundleRelease` (génère un `.aab`)
2. Signe le bundle (keystore)
3. Téléverse sur la Google Play Console

## 🍏 iOS

Capacitor supporte aussi iOS (nécessite **macOS + Xcode**) :
```bash
npm install @capacitor/ios
npx cap add ios
npx cap open ios
```

## 🎨 Personnalisation

- **Icône** : remplace `www/icons/icon-512.png` (et 192) puis, pour Android,
  régénère les icônes natives (`npx @capacitor/assets generate`).
- **Nom / couleurs** : `capacitor.config.json` et `www/manifest.webmanifest`.

## ✅ Vérifié

- Service worker enregistré (`getRegistrations() === 1`) → PWA installable / hors-ligne.
- Rendu mobile (390×844) validé : connexion, inscription, dashboard, factures.
- Projet Android scaffoldé par Capacitor (`android/` + Gradle) ; compilation
  déléguée à la CI faute d'accès au SDK Google en local.
