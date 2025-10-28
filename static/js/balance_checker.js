function balanceChecker(balanceEndpoint, isAuthenticated) {
    return {
        balance: null,
        open: false,
        pollingInterval: null,
        pollingRate: 10 * 1000, // 10 seconds by default
        defaultRate: 10 * 60 * 1000, //10 minutes

        async balancePolling() {
            if (!isAuthenticated) {
                return
            }
            await this.fetchBalance();
            this.startPolling();
        },

        async fetchBalance() {
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
            this.pollingRate = this.defaultRate;
            this.startPolling();
        }
    }
}