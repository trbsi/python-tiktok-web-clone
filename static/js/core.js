document.addEventListener('alpine:init', () => {
    Alpine.magic('utils', () => ({
        getCsrfToken() {
            return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        },
    }))
});

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

