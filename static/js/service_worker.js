self.addEventListener("install", e => {
    console.log("Service Worker Installed.");
});

self.addEventListener("activate", e => {
    console.log("Service Worker Activated.");
});

self.addEventListener("push", event => {
    const data = event.data.json();
    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: "/static/images/icon-192.png",
            badge: "/static/images/icon-192.png",
            data: {url: data.url}
        })
    );
});

self.addEventListener("notificationclick", event => {
    event.notification.close();
    event.waitUntil(clients.openWindow(event.notification.data.url));
});
