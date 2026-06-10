// Preload minimal — expose une petite API sûre au front si besoin futur.
// Pour l'instant l'app fonctionne entièrement avec localStorage côté page,
// donc aucune passerelle n'est nécessaire. Le fichier est gardé pour
// l'isolation de contexte (contextIsolation: true) et l'évolutivité.

const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("desktop", {
    isDesktopApp: true,
    platform: process.platform,
});
