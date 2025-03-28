const CACHE_NAME = 'cyber-crime-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js',
  '/static/images/error.jpg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
});