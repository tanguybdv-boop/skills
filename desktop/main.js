// ============================================================
//  Comptabilité Pro — Application de bureau (Electron)
//  Processus principal : crée la fenêtre, le menu, gère le cycle de vie.
// ============================================================

const { app, BrowserWindow, Menu, shell, dialog } = require("electron");
const path = require("path");

const ENTRY = path.join(__dirname, "web", "comptabilite_client_portail.html");
const PRODUCT_NAME = "Comptabilité Pro";

let mainWindow = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 860,
        minWidth: 900,
        minHeight: 640,
        backgroundColor: "#0a0d14",
        title: PRODUCT_NAME,
        icon: path.join(__dirname, "assets", "icon.png"),
        autoHideMenuBar: false,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false,
            // Autorise la navigation entre les fichiers HTML locaux (portail -> compta)
            sandbox: false,
        },
    });

    mainWindow.loadFile(ENTRY);

    // Ouvrir les liens externes (http/https) dans le navigateur système, pas dans l'app
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        if (url.startsWith("http://") || url.startsWith("https://")) {
            shell.openExternal(url);
            return { action: "deny" };
        }
        return { action: "allow" };
    });

    mainWindow.on("closed", () => { mainWindow = null; });
}

function buildMenu() {
    const isMac = process.platform === "darwin";

    const template = [
        ...(isMac ? [{
            label: app.name,
            submenu: [
                { role: "about", label: "À propos" },
                { type: "separator" },
                { role: "hide", label: "Masquer" },
                { role: "quit", label: "Quitter" },
            ],
        }] : []),
        {
            label: "Fichier",
            submenu: [
                {
                    label: "Accueil (Portail)",
                    accelerator: "CmdOrCtrl+H",
                    click: () => { if (mainWindow) mainWindow.loadFile(ENTRY); },
                },
                {
                    label: "Comptabilité complète",
                    accelerator: "CmdOrCtrl+K",
                    click: () => {
                        if (mainWindow) mainWindow.loadFile(path.join(__dirname, "web", "comptabilite_autoentrepreneur.html"));
                    },
                },
                { type: "separator" },
                isMac ? { role: "close", label: "Fermer" } : { role: "quit", label: "Quitter" },
            ],
        },
        {
            label: "Édition",
            submenu: [
                { role: "undo", label: "Annuler" },
                { role: "redo", label: "Rétablir" },
                { type: "separator" },
                { role: "cut", label: "Couper" },
                { role: "copy", label: "Copier" },
                { role: "paste", label: "Coller" },
                { role: "selectAll", label: "Tout sélectionner" },
            ],
        },
        {
            label: "Affichage",
            submenu: [
                { role: "reload", label: "Recharger" },
                { role: "resetZoom", label: "Zoom normal" },
                { role: "zoomIn", label: "Agrandir" },
                { role: "zoomOut", label: "Réduire" },
                { type: "separator" },
                { role: "togglefullscreen", label: "Plein écran" },
                { role: "toggleDevTools", label: "Outils de développement" },
            ],
        },
        {
            label: "Aide",
            submenu: [
                {
                    label: "À propos de " + PRODUCT_NAME,
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: "info",
                            title: "À propos",
                            message: PRODUCT_NAME,
                            detail:
                                "Logiciel de comptabilité pour autoentrepreneur.\n" +
                                "Factures clients/fournisseurs, URSSAF, TVA, déclarations.\n\n" +
                                "Données stockées localement sur votre machine.\n" +
                                "Version " + app.getVersion(),
                            buttons: ["OK"],
                        });
                    },
                },
            ],
        },
    ];

    Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

app.whenReady().then(() => {
    buildMenu();
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
