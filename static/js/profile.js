function userProfile(reportContentApi) {
    return {
        menuOpen: false,
        showReportForm: false,
        reportDescription: "",
        reportTarget: null,

        openReportForm(reportTarget) {
            this.reportTarget = reportTarget;
            this.showReportForm = true;
        },

        closeReportForm() {
            this.showReportForm = false;
            this.reportDescription = '';
            this.targetMedia = null;
        },

        async submitReport() {
            if (!this.reportTarget) return;

            try {
                if (Number.isInteger(this.reportTarget)) {
                    reportTargetId = this.reportTarget
                } else {
                    reportTargetId = this.reportTarget.id
                }

                const res = await fetch(reportContentApi, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.$utils.getCsrfToken(),
                    },
                    body: JSON.stringify({
                        type: 'user',
                        content_id: reportTargetId,
                        description: this.reportDescription
                    }),
                    credentials: 'include'
                });

                if (!res.ok) throw new Error('Report failed');
                await res.json();

                alert('Thanks for your feedback. We’ll review this content shortly.');
                this.showReportForm = false;
                this.reportDescription = "";
                this.reportTarget = null;
            } catch (e) {
                console.error(e);
            }
        }
    };
}