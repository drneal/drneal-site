// drnealaggarwal.info — Service Worker
// Caches app shells for offline use; network-first for API calls.

const CACHE = 'dna-v2';
const SHELL = [
  '/voice-notes',
  '/dr-detector',
  '/static/css/style.css',
  '/static/dr-detector-manifest.json',
  '/static/dr-detector-icon-192.png',
  '/static/dr-detector-icon-512.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Network-first for API calls
  if (url.pathname.startsWith('/voice-notes/format')) {
    e.respondWith(fetch(e.request));
    return;
  }
  // Cache-first for shell assets
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
