// Service Worker — Comptabilité Pro (PWA)
// Stratégie : cache-first sur le "shell" de l'app pour un fonctionnement hors-ligne.
const CACHE = "comptapro-v1";
const ASSETS = [
    "./",
    "./index.html",
    "./comptabilite_autoentrepreneur.html",
    "./manifest.webmanifest",
    "./icons/icon-192.png",
    "./icons/icon-512.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    const { request } = event;
    if (request.method !== "GET") return;
    event.respondWith(
        caches.match(request).then((cached) => {
            if (cached) return cached;
            return fetch(request)
                .then((resp) => {
                    // Met en cache les nouvelles ressources même origine
                    const copy = resp.clone();
                    if (resp.ok && new URL(request.url).origin === self.location.origin) {
                        caches.open(CACHE).then((c) => c.put(request, copy));
                    }
                    return resp;
                })
                .catch(() => cached);
        })
    );
});
