function balanceChecker(balanceEndpoint, isAuthenticated) {
    return {
        balance: null,
        open: false,
        pollingInterval: null,
        pollingRate: 1 * 60 * 1000, // 1 minute
        storage_key: 'balance_checker',

        async balancePolling() {
            if (!isAuthenticated) {
                return
            }
            await this.fetchBalance();
            this.startPolling();
        },

        async fetchBalance() {
            console.log('Balance checked');
            if (this.getWithExpiry() !== null) {
                return;
            }

            try {
                const res = await fetch(balanceEndpoint);
                const data = await res.json();
                this.balance = data.balance;

                if (data.status === 'low_balance') {
                    this.open = true;
                } else if (data.status === 'hide') {
                    this.stopPolling();
                }

            } catch (err) {
                console.error('Balance check failed:', err);
            }
        },

        startPolling() {
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
            }

            // Start a new one with the current pollingRate
            this.pollingInterval = setInterval(() => {
                this.fetchBalance();
            }, this.pollingRate);
        },

        stopPolling() {
            clearInterval(this.pollingInterval);
        },

        closePopup() {
            this.open = false;
            this.setWithExpiry();
            this.startPolling();
        },

        setWithExpiry() {
            const now = Date.now();
            const item = {
                value: true,
                expiry: now + 5 * 60 * 1000, //5 minutes
            };
            localStorage.setItem(this.storage_key, JSON.stringify(item));
        },

        getWithExpiry() {
            const itemStr = localStorage.getItem(this.storage_key);
            if (!itemStr) return null;

            const item = JSON.parse(itemStr);
            const now = Date.now();

            if (now > item.expiry) {
                localStorage.removeItem(this.storage_key);
                return null;
            }

            return item.value;
        }
    }
}