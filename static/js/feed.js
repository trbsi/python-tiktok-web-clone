function videoFeed() {
    return {
        videos: [],                // list of video objects
        page: 1,                   // pagination
        loadingMore: false,
        hasMore: true,
        currentIndex: 0,
        observer: null,
        progress: {},              // progress per index (0..100)
        loadingVideo: {},          // buffering flags per index
        commentsOpen: false,
        comments: [],
        commentsLoading: false,
        commentInput: '',
        activeVideo: null,         // currently opened video for comments
        perPage: 10,               // how many videos per fetch

        init() {
            // initial load
            this.loadMore();

            // set up an IntersectionObserver to detect which video is in view
            // We'll create the observer after a short delay so DOM nodes exist after first load.
            this.$nextTick(() => {
                // observe via polling for refs available
                const waitForRefs = () => {
                    if (!this.$refs.video || !this.$refs.video.length) {
                        setTimeout(waitForRefs, 100);
                        return;
                    }
                    this.setupObserver();
                };
                waitForRefs();
            });

            // pause all videos on page load, then play the top-most after a tiny delay for autoplay to work consistently
            window.addEventListener('visibilitychange', () => {
                if (document.hidden) this.pauseAll();
                else this.playCurrent();
            });
        },

        async loadMore() {
            if (this.loadingMore || !this.hasMore) return;
            this.loadingMore = true;
            try {
                const res = await fetch(`/api/videos?page=${this.page}&per_page=${this.perPage}`);
                if (!res.ok) throw new Error('Failed to fetch videos');
                const data = await res.json();

                // expected response shape: { results: [...], next_page: 2/null }
                const items = data.results || data;
                items.forEach(v => {
                    // normalize fields we use:
                    v.likes = v.likes ?? 0;
                    v.liked = !!v.liked;
                    v.comments_count = v.comments_count ?? 0;
                    v.user = v.user || {username: 'unknown', avatar: 'https://via.placeholder.com/150'};
                    v.description = v.description ?? '';
                });

                this.videos = this.videos.concat(items);
                this.page = data.next_page ?? (this.page + 1);
                this.hasMore = !!data.next_page;

                // after adding new items we need to re-run observer
                this.$nextTick(() => {
                    if (this.observer) {
                        this.$refs.video.forEach(el => this.observer.observe(el));
                    } else {
                        this.setupObserver();
                    }
                });
            } catch (e) {
                console.error(e);
            } finally {
                this.loadingMore = false;
            }
        },

        setupObserver() {
            // clean up if exists
            if (this.observer) {
                try {
                    this.$refs.video.forEach(el => this.observer.unobserve(el));
                } catch (e) {
                }
                this.observer.disconnect();
            }

            // Options tuned so video considered "in view" when >=60% visible
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
                    if (this.videos.length - index <= 5) {
                        this.loadMore();
                    }
                } else {
                    // not enough visible
                    // optional: pause
                    // this.pauseAtIndex(index)
                }
            }, {threshold: [0, 0.25, 0.5, 0.6, 0.75, 1]});

            // observe all current video nodes
            this.$refs.video.forEach(el => this.observer.observe(el));
        },

        playAtIndex(index) {
            // pause all
            this.$refs.video.forEach((v, i) => {
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
                        this.progress[i] = 0;
                    }
                } catch (e) {
                    console.error(e);
                }
            });
        },

        pauseAll() {
            if (!this.$refs.video) return;
            this.$refs.video.forEach(v => {
                try {
                    v.pause();
                } catch (e) {
                }
            });
        },

        playCurrent() {
            this.playAtIndex(this.currentIndex || 0);
        },

        updateProgress(index, event) {
            const video = event.target;
            if (!video.duration) return;
            this.progress[index] = Math.round((video.currentTime / video.duration) * 100);
        },

        onVideoLoaded(index) {
            // called when metadata/frames loaded; hide spinner if set
            this.loadingVideo[index] = false;
        },

        onScroll() {
            // placeholder in case we want to handle touch scrolling specifics
        },

        formatCount(n) {
            if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
            if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
            return n;
        },

        async toggleLike(video, index) {
            // Optimistic UI
            const previousLiked = video.liked;
            const previousLikes = video.likes;
            video.liked = !video.liked;
            video.likes += video.liked ? 1 : -1;

            try {
                const res = await fetch(`/api/videos/${video.id}/like`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({like: video.liked}),
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Like failed');
                // optionally update counts from server response
                const data = await res.json();
                if (data.likes != null) video.likes = data.likes;
            } catch (e) {
                // rollback
                video.liked = previousLiked;
                video.likes = previousLikes;
                console.error(e);
                alert('Failed to update like. Try again.');
            }
        },

        async openComments(video) {
            this.commentsOpen = true;
            this.activeVideo = video;
            this.comments = [];
            this.commentInput = '';
            this.commentsLoading = true;

            try {
                const res = await fetch(`/api/videos/${video.id}/comments`);
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
            this.activeVideo = null;
        },

        async submitComment() {
            if (!this.activeVideo) return;
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
            this.activeVideo.comments_count = (this.activeVideo.comments_count || 0) + 1;

            try {
                const res = await fetch(`/api/videos/${this.activeVideo.id}/comments`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                if (!res.ok) throw new Error('Failed to post comment');
                const saved = await res.json();
                // replace temp comment with saved comment (if server returns it)
                // naive approach: replace first temp id
                const idx = this.comments.findIndex(c => c.id === temp.id);
                if (idx !== -1 && saved) this.comments.splice(idx, 1, saved);
            } catch (e) {
                // rollback UI changes
                this.comments = this.comments.filter(c => c.id !== temp.id);
                this.activeVideo.comments_count = Math.max(0, (this.activeVideo.comments_count || 1) - 1);
                alert('Failed to post comment.');
                console.error(e);
            }
        },

        openProfile(user) {
            // open user profile - replace with your routing
            // If you use client-side routing, navigate there instead.
            window.location.href = `/users/${encodeURIComponent(user.username)}`;
        },

        async shareVideo(video) {
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
        }
    };
}
