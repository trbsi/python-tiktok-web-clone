$(document).ready(function() {
    const LATER_COOLDOWN_HOURS = 1;

    function shouldShowPopup() {
        if (localStorage.getItem("pushAccepted") === "true") return false;

        const lastDenied = localStorage.getItem("pushDeniedAt");
        if (lastDenied) {
            const diffHours = (Date.now() - Number(lastDenied)) / (1000*60*60);
            if (diffHours < LATER_COOLDOWN_HOURS) return false;
        }

        if (Notification.permission === "granted") {
            localStorage.setItem("pushAccepted", "true");
            return false;
        }

        return true;
    }

    // Show popup if needed
    if (shouldShowPopup()) {
        $("#pushPopup").removeClass("hidden");
    }

    // "Maybe Later" button
    $("#pushDeny, #closePushPopup").click(function() {
        $("#pushPopup").addClass("hidden");
        localStorage.setItem("pushDeniedAt", Date.now());
    });

    // "Allow" button
    $("#pushAllow").click(async function() {
        $("#pushPopup").addClass("hidden");
        localStorage.setItem("pushAccepted", "true");

        const permission = await Notification.requestPermission();
        if (permission !== "granted") {
            alert("Please allow notifications in your browser settings.");
            return;
        }

        // Register service worker
        const sw = await navigator.serviceWorker.register("/service-worker.js");

        // Fetch VAPID public key from backend
        //serviceWorkerFile is defined in js.html
        const vapidPublicKey = await $.get(serviceWorkerFile);

        const subscription = await sw.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
        });

        // Send subscription to backend
        await $.ajax({
            url: "/save-subscription",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(subscription)
        });

        console.log("Push subscribed:", subscription);
    });

    // Utility function to convert base64 VAPID key
    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
        const rawData = window.atob(base64);
        return new Uint8Array([...rawData].map(c => c.charCodeAt(0)));
    }
});
