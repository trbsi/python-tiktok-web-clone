function discoverFeed(discoverFeedUrl, mediaApiUrl, query, filters) {
    return {
        mediaList: [],
        filterQuery: '',
        loadingMore: false,
        hasMore: true,
        page: 1, // pagination
        feedType: 'discover',

        init() {
            this.filterQuery = query;
            this.loadMore();

            // IntersectionObserver for infinite scroll
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && entry.target === this.$refs.sentinel) {
                        this.loadMore();
                    }
                });
            }, {
                rootMargin: '200px'
            });

            observer.observe(this.$refs.sentinel);
        },

        async loadMore() {
            if (this.loadingMore || !this.hasMore) {
                return;
            }

            this.loadingMore = true;

            try {
                const res = await fetch(`${mediaApiUrl}?page=${this.page}&type=${this.feedType}&filters=${filters}`);
                if (!res.ok) throw new Error('Failed to fetch media');
                const data = await res.json();

                // expected response shape: { results: [...], next_page: 2/null }
                const items = data.results;
                this.mediaList = [...this.mediaList, ...items];

                this.page = data.next_page ?? (this.page + 1);
                this.hasMore = !!data.next_page;

                if (this.hasMore) {
                    this.page = data.next_page;
                }
            } catch (e) {
                console.error(e);
            } finally {
                this.loadingMore = false;
            }
        },

        filterDiscover() {
            if (!this.filterQuery) {
                return
            }

            url = discoverFeedUrl + '?query=' + this.filterQuery
            window.location = url
        },

        resetFilter() {
            window.location = discoverFeedUrl
        },

        openProfile(user) {
            // userProfileUrl comes from js.html
            window.location = userProfileUrl.replace('__PLACEHOLDER__', user.username);
        },
    };
}