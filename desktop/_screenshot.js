// Utilitaire de dev : lance l'app en headless (xvfb) et capture des PNG.
// Usage: electron _screenshot.js <htmlRelPath> <outPng> [injectJsFile]
const { app, BrowserWindow } = require("electron");
const path = require("path");
const fs = require("fs");

// Ignore les flags Electron (ex: --no-sandbox) et le nom du script lui-même,
// qui peuvent rester dans argv selon la façon dont Electron est invoqué.
// (On garde les éventuels fichiers d'injection .js passés en argument.)
const positional = process.argv
    .slice(1)
    .filter(a => !a.startsWith("-") && path.basename(a) !== "_screenshot.js");
const htmlRel = positional[0] || "web/comptabilite_client_portail.html";
const outPng = positional[1] || "shot.png";
const injectFile = positional[2] || null;

// Sécurité : refuse d'écrire la sortie sur un .html (évite d'écraser une page)
if (outPng.toLowerCase().endsWith(".html")) {
    console.error("Refus: la sortie ne doit pas être un .html →", outPng);
    process.exit(1);
}

app.whenReady().then(async () => {
    const win = new BrowserWindow({
        width: 1280, height: 860, show: false,
        backgroundColor: "#0a0d14",
        webPreferences: { preload: path.join(__dirname, "preload.js"), contextIsolation: true, sandbox: false },
    });

    await win.loadFile(path.join(__dirname, htmlRel));

    if (injectFile && fs.existsSync(injectFile)) {
        const js = fs.readFileSync(injectFile, "utf8");
        try { const r = await win.webContents.executeJavaScript(js, true); console.log("inject return:", r); } catch (e) { console.error("inject err", e.message); }
    }

    // Laisser le rendu/anim se stabiliser
    await new Promise(r => setTimeout(r, 600));

    const img = await win.webContents.capturePage();
    fs.writeFileSync(outPng, img.toPNG());
    console.log("écrit:", outPng);
    app.quit();
});
