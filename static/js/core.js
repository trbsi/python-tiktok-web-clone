document.addEventListener('alpine:init', () => {
    Alpine.magic('utils', () => ({
        getCsrfToken() {
            return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        },

        async canSpend(type) {
            try {
                const response = await fetch('/payment/api/can-purchase', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.getCsrfToken()
                        },
                        body: JSON.stringify({type: type})
                    }
                );

                const json = await response.json()
                if (!response.ok) {
                    throw json;
                }

                return {'ok': true}

            } catch (error) {
                return {'ok': false, 'error': error.error}
            }
        }
    }))
});

