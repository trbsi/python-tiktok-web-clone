function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

/* ------------- PWA site - install website on phone -------------  */
if ("serviceWorker" in navigator) {
    //serviceWorkerFile is defined in head.html
    navigator.serviceWorker.register(serviceWorkerFile);
}

let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault(); // prevent default mini-infobar
    deferredPrompt = e;

    // Show your custom install button
    $("#installBanner").removeClass("hidden");
});

// iOS does not fire beforeinstallprompt and does not allow programmatic prompts.
const isIOS = /iphone|ipad|ipod/i.test(window.navigator.userAgent);
const isInStandalone = ("standalone" in window.navigator) && window.navigator.standalone;

if (isIOS && !isInStandalone) {
    $("#iosInstallHint").removeClass("hidden");
}


$("#installBtn").on("click", async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const choice = await deferredPrompt.userChoice;

    if (choice.outcome === "accepted") {
        console.log("User installed the app");
    } else {
        console.log("User dismissed the install prompt");
    }

    deferredPrompt = null;
    $("#installBanner").addClass("hidden");
});
