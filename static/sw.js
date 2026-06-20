// Voice Clinical Notes — Service Worker
// Caches the app shell for offline use; network-first for API calls.

const CACHE = 'vcn-v1';
const SHELL = ['/voice-notes', '/static/css/style.css'];

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
