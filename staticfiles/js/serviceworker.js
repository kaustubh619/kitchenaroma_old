// Cache on install

var staticCacheName = 'djangopwa-v1';
self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(staticCacheName).then(function(cache) {
        return cache.addAll([
          '',
        ]);
      })
    );
  });

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
      caches.keys().then(cacheNames => {
          return Promise.all(
              cacheNames
                  .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                  .filter(cacheName => (cacheName !== staticCacheName))
                  .map(cacheName => caches.delete(cacheName))
          );
      })
  );
});

// Serve from Cache
self.addEventListener("fetch", event => {
  event.respondWith(
      caches.match(event.request)
          .then(response => {
              return response || fetch(event.request);
          })
          .catch(() => {
              return caches.match('offline');
          })
  )
});