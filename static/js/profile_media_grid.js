function profileGrid(username, mediaApiUrl) {
    return {
        mediaList: [],
        page: 1,
        loading: false,
        hasMore: true,
        perPage: 12,

        init() {
            this.loadMedia();

            // Infinite scroll observer
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && entry.target === this.$refs.sentinel) {
                        if (!this.loading && this.hasMore) {
                            this.loadMedia();
                        }
                    }
                });
            }, {rootMargin: '200px'});
            observer.observe(this.$refs.sentinel)
        },

        async loadMedia() {
            if (this.loading || !this.hasMore) return;
            this.loading = true;

            try {
                // Example API endpoint – adjust to your backend
                const res = await fetch(`${mediaApiUrl}?page=${this.page}&username=${username}`);
                if (!res.ok) throw new Error("Failed to load media");

                const data = await res.json();
                const items = data.results || data;
                this.mediaList.push(...items);

                this.page = data.next_page ?? (this.page + 1);
                this.hasMore = !!data.next_page;
            } catch (e) {
                console.error(e);
            } finally {
                this.loading = false;
            }
        },

        formatCount(value, mediaType) {
            if (!(typeof value === 'number')) {
                if (mediaType === 'image') {
                    return '<i class="ri-image-line"></i>';
                }

                if (mediaType === 'video') {
                    return '<i class="ri-video-on-line"></i>';
                }

                return value
            }

            if (value >= 1e6) return (value / 1e6).toFixed(1) + "M";
            if (value >= 1e3) return (value / 1e3).toFixed(1) + "K";
            return value;
        }
    }
}
