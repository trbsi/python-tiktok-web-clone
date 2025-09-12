function mediaFeed() {
    return {
        media: [],                // list of video objects
        page: 1,                   // pagination
        loadingMore: false,
        hasMore: true,
        currentIndex: 0,
        observer: null,
        progressBar: {},              // progress per index (0..100)
        loadingVideo: {},          // buffering flags per index
        commentsOpen: false,
        comments: [],
        commentsLoading: false,
        commentInput: '',
        activeMedia: null,         // currently opened video for comments
        isMuted: true,

        init() {
            // initial load
            this.loadMore();

            // pause all media on page load, then play the top-most after a tiny delay for autoplay to work consistently
            window.addEventListener('visibilitychange', () => {
                if (document.hidden) this.pauseAll();
                else this.playCurrent();
            });
        },

        async loadMore() {
            if (this.loadingMore || !this.hasMore) {
                return;
            }

            this.loadingMore = true;
            try {
                const res = await fetch(`/feed/api/media?page=${this.page}`);
                if (!res.ok) throw new Error('Failed to fetch media');
                const data = await res.json();

                // expected response shape: { results: [...], next_page: 2/null }
                const items = data.results || data;
                this.media = this.media.concat(items);
                this.page = data.next_page ?? (this.page + 1);
                this.hasMore = !!data.next_page;
            } catch (e) {
                console.error(e);
            } finally {
                this.loadingMore = false;

                // after adding new items we need to re-run observer
                this.$nextTick(() => {
                    if (this.observer) {
                        this.getMedia().forEach(el => this.observer.observe(el));
                    } else {
                        this.setupObserver();
                    }
                });
            }
        },

        getMedia() {
            return this.$root.querySelectorAll('[x-ref="media"]');
        },

        getSingleMedia(index) {
            return this.$root.querySelectorAll('[x-ref="media"]')[index];
        },

        setupObserver() {
            // clean up if exists
            if (this.observer) {
                try {
                    this.getMedia().forEach(el => this.observer.unobserve(el));
                } catch (e) {
                }
                this.observer.disconnect();
            }

            // Options tuned so media considered "in view" when >=60% visible
            this.observer = new IntersectionObserver((entries) => {
                // choose the entry with highest intersectionRatio
                let best = null;
                entries.forEach(entry => {
                    if (!best || entry.intersectionRatio > best.intersectionRatio) best = entry;
                });
                if (!best) return;

                // find index for the entry target
                const index = parseInt(best.target.getAttribute('data-index'));
                if (best.intersectionRatio >= 0.6) {
                    // pause other videos, play this one
                    this.currentIndex = index;
                    this.playAtIndex(index);
                    // if we are 5th before end, load more
                    if (this.media.length - index <= 5) {
                        this.loadMore();
                    }
                } else {
                    // not enough visible
                    // optional: pause
                    this.pauseAtIndex(index)
                }
            }, {threshold: [0, 0.25, 0.5, 0.6, 0.75, 1]});

            // observe all current media nodes
            this.getMedia().forEach(el => this.observer.observe(el))
        },

        playAtIndex(index) {
            console.log('index', index)
            // pause all
            this.getMedia().forEach((v, i) => {
                try {
                    if (i === index) {
                        // ensure we attempt to play; browsers require muted for autoplay
                        this.loadingVideo[i] = true;
                        v.muted = true;
                        const playPromise = v.play();
                        if (playPromise && playPromise.then) {
                            playPromise.then(() => {
                                this.loadingVideo[i] = false;
                            }).catch(() => {
                                this.loadingVideo[i] = false;
                            });
                        } else {
                            this.loadingVideo[i] = false;
                        }
                        v.loop = true;
                    } else {
                        v.pause();
                        v.currentTime = 0; // optional: rewind off-screen videos
                        this.progressBar[i] = 0;
                    }
                } catch (e) {
                    console.error(e);
                }
            });
        },

        pauseAtIndex(index) {
            const video = this.getSingleMedia(index)
            if (!video) return;

            try {
                video.pause();
                this.progressBar[index] = 0;
            } catch (e) {
                console.error(`Failed to pause video at index ${index}`, e);
            }
        },

        pauseAll() {
            this.getMedia().forEach(v => {
                try {
                    v.pause();
                } catch (e) {
                }
            });
        },

        muteAll() {
            if (!this.getMedia()) return;
            this.getMedia().forEach(video => {
                video.muted = true;
            });
            this.isMuted = true;
        },

        unmuteAll() {
            if (!this.getMedia()) return;
            this.getMedia().forEach(video => {
                video.muted = false;
            });
            this.isMuted = false
        },

        playCurrent() {
            this.playAtIndex(this.currentIndex || 0);
        },

        updateProgress(index, event) {
            const video = event.target;
            if (!video.duration) return;
            this.progressBar[index] = Math.round((video.currentTime / video.duration) * 100);
        },

        onVideoLoaded(index) {
            // called when metadata/frames loaded; hide spinner if set
            this.loadingVideo[index] = false;
        },

        onScroll() {
            console.log('asdasdasd')
        },

        formatCount(n) {
            if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
            if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
            return n;
        },

        togglePlay(index) {
            var video = this.getSingleMedia(index)
            if (!video) {
                return;
            }

            if (video.paused) {
                this.pauseAll()
                this.currentIndex = index
                this.playAtIndex(index)
            } else {
                video.pause()
            }
        },

        async toggleLike(media, index) {
            // Optimistic UI
            const previousLiked = media.liked;
            const previousLikes = media.likes;
            media.liked = !media.liked;
            media.likes += media.liked ? 1 : -1;

            try {
                const res = await fetch(`/engagement/api/like/media/${media.id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': this.getCsrfToken(),},
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Like failed');
                // optionally update counts from server response
                const data = await res.json();
                if (data.likes != null) media.likes = data.likes;
            } catch (e) {
                // rollback
                media.liked = previousLiked;
                media.likes = previousLikes;
                console.error(e);
                alert('Failed to update like. Try again.');
            }
        },

        follow() {

        },

        async openComments(media) {
            this.commentsOpen = true;
            this.activeMedia = media;
            this.comments = [];
            this.commentInput = '';
            this.commentsLoading = true;

            try {
                const res = await fetch(`/engagement/api/comments/media/${media.id}`);
                if (!res.ok) throw new Error('Failed to fetch comments');
                const data = await res.json();
                this.comments = data.results || data;
            } catch (e) {
                console.error(e);
                alert('Failed to load comments.');
            } finally {
                this.commentsLoading = false;
            }
        },

        closeComments() {
            this.commentsOpen = false;
            this.activeMedia = null;
        },

        async submitComment() {
            if (!this.activeMedia) return;
            const text = this.commentInput.trim();
            if (!text) return;

            // optimistic add
            const temp = {
                id: 'temp-' + Date.now(),
                text,
                user: {username: 'You', avatar: '/path/to/avatar.png'},
                created_at: 'just now'
            };
            this.comments.unshift(temp);
            this.commentInput = '';
            // increment comments_count in UI
            this.activeMedia.comments_count = (this.activeMedia.comments_count || 0) + 1;

            var body = {
                'media_id': this.activeMedia.id,
                'comment': text
            }

            try {
                const res = await fetch(`/engagement/api/comments`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': this.getCsrfToken()},
                    body: JSON.stringify(body)
                });
                if (!res.ok) throw new Error('Failed to post comment');
                const saved = await res.json();
                // replace temp comment with saved comment (if server returns it)
                // naive approach: replace first temp id
                const idx = this.comments.findIndex(comment => comment.id === temp.id);
                if (idx !== -1 && saved) {
                    this.comments.splice(idx, 1, saved);
                }
            } catch (e) {
                // rollback UI changes
                this.comments = this.comments.filter(comment => comment.id !== temp.id);
                this.activeMedia.comments_count = Math.max(0, (this.activeMedia.comments_count || 1) - 1);
                console.error(e);
            }
        },

        openProfile(user) {
            // open user profile - replace with your routing
            // If you use client-side routing, navigate there instead.
            window.location.href = `/user/${encodeURIComponent(user.username)}`;
        },

        async shareMedia(video) {
            const shareData = {
                title: 'Check out this video',
                text: video.description || '',
                url: window.location.origin + '/videos/' + video.id
            };
            try {
                if (navigator.share) {
                    await navigator.share(shareData);
                } else {
                    // fallback: copy url
                    await navigator.clipboard.writeText(shareData.url);
                    alert('Link copied to clipboard');
                }
            } catch (e) {
                console.error('Share failed', e);
                alert('Unable to share on this device.');
            }
        },

        async reportMedia(media) {
            if (!confirm('Are you sure?')) {
                return
            }

            try {
                const res = await fetch(`/report/api/report`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': this.getCsrfToken(),},
                    body: JSON.stringify({'type': 'media', 'content_id': media.id}),
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Report failed');
                // optionally update counts from server response
                const data = await res.json();
                alert('Content has been reported. We will review it.');
            } catch (e) {
                console.error(e);
            }
        },

        getCsrfToken() {
            return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        }
    };
}
