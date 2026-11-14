'use strict';
const CACHE='tlc-app-shell-v4';
const SHELL=['/app/','/app/app.css','/app/app.js?v=20261114-share-start','/app/manifest.webmanifest','/app/icons/icon-192.png','/app/icons/icon-512.png','/app/icons/apple-touch-icon.png','/assets/brand/tlc-white.webp','/assets/brand/carmen-silhouette.webp','/assets/brand/clue-calendar.webp','/assets/brand/clue-business-card.webp'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL)));});
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('tlc-app-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{const u=new URL(event.request.url);if(event.request.method!=='GET'||u.origin!==self.location.origin)return;
// Never cache event records, forms, credentials, or member content.
if(event.request.mode==='navigate'&&u.pathname.startsWith('/app/')){event.respondWith(fetch(event.request).catch(()=>caches.match('/app/')));return;}
const shellKey=u.pathname+u.search;
if(SHELL.includes(shellKey)){event.respondWith(fetch(event.request,{cache:'no-cache'}).then(response=>{if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(shellKey,copy)));}return response;}).catch(()=>caches.match(shellKey)));}});

