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
                expiry: now + 10 * 60 * 1000, //10 minutes
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

async function canSpend(type) {
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

        let oldBalance = json.balance
        const intervalId = setInterval(async () => {
            const response = await fetch('/payment/api/balance');
            const json = await response.json();
            const newBalance = json.balance;
            console.log('new', newBalance)
            console.log('old', oldBalance)
            if (newBalance != oldBalance) {
                showBalanceNotification(newBalance);
                clearInterval(intervalId);
            }
        }, 5000);

        return {'ok': true}

    } catch (error) {
        return {'ok': false, 'error': error.error}
    }
}

function showBalanceNotification(change) {
    var notification = $("#balance-notification");

    // Update the text dynamically
    notification.text(change + " coins left");

    // Change color depending on positive or negative
    notification.removeClass("bg-green-500/90 bg-red-500/90")
        .addClass(change > 0 ? "bg-green-500/90" : "bg-red-500/90");

    // Show the div
    notification.removeClass("hidden");

    // Trigger reflow to restart animation
    void notification[0].offsetWidth;

    // Add animation class
    notification.addClass("animate-fadeUp");

    // Hide after animation duration (5s)
    setTimeout(function () {
        notification.addClass("hidden");
        notification.removeClass("animate-fadeUp");
    }, 5000);
}
