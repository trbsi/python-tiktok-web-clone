function videoFeed() {
    return {
        videos: [],                // list of video objects
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
        activeVideo: null,         // currently opened video for comments
        perPage: 10,               // how many videos per fetch
        isMuted: true,

        init() {
            // initial load
            this.loadMore();

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
                const res = await fetch(`/feed/api/videos?page=${this.page}&per_page=${this.perPage}`);
                if (!res.ok) throw new Error('Failed to fetch videos');
                const data = await res.json();

                // expected response shape: { results: [...], next_page: 2/null }
                const items = data.results || data;
                items.forEach(v => {
                    // normalize fields we use:
                    v.like_count = v.like_count;
                    v.liked = !!v.liked;
                    v.comments_count = v.comments_count;
                    v.user = v.user || {username: 'unknown', avatar: 'https://via.placeholder.com/150'};
                    v.description = v.description ?? '';
                    v.src = v.src;
                    v.id = v.id;
                });

                this.videos = this.videos.concat(items);
                this.page = data.next_page ?? (this.page + 1);
                this.hasMore = !!data.next_page;
            } catch (e) {
                console.error(e);
            } finally {
                this.loadingMore = false;

                // after adding new items we need to re-run observer
                this.$nextTick(() => {

                    if (this.observer) {
                        this.getVideos().forEach(el => this.observer.observe(el));
                    } else {
                        this.setupObserver();
                    }
                });
            }
        },

        getVideos() {
            return this.$root.querySelectorAll('[x-ref="video"]');
        },

        getVideo(index) {
            return this.$root.querySelectorAll('[x-ref="video"]')[index];
        },

        setupObserver() {
            // clean up if exists
            if (this.observer) {
                try {
                    this.getVideos().forEach(el => this.observer.unobserve(el));
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
                    this.pauseAtIndex(index)
                }
            }, {threshold: [0, 0.25, 0.5, 0.6, 0.75, 1]});

            // observe all current video nodes
            this.getVideos().forEach(el => this.observer.observe(el))
        },

        playAtIndex(index) {
            // pause all
            this.getVideos().forEach((v, i) => {
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
            const video = this.getVideo(index)
            if (!video) return;

            try {
                video.pause();
                this.progressBar[index] = 0;
            } catch (e) {
                console.error(`Failed to pause video at index ${index}`, e);
            }
        },


        pauseAll() {
            this.getVideos().forEach(v => {
                try {
                    v.pause();
                } catch (e) {
                }
            });
        },

        muteAll() {
            if (!this.getVideos()) return;
            this.getVideos().forEach(video => {
                video.muted = true;
            });
            this.isMuted = true;
        },

        unmuteAll() {
            if (!this.getVideos()) return;
            this.getVideos().forEach(video => {
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
            // placeholder in case we want to handle touch scrolling specifics
        },

        formatCount(n) {
            if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
            if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
            return n;
        },

        togglePlay(index) {
            var video = this.getVideo(index)
            if (!video) return;

            if (video.paused) {
                this.pauseAll()
                this.currentIndex = index
                this.playAtIndex(index)
            } else {
                video.pause()
            }
        },

        async toggleLike(video, index) {
            // Optimistic UI
            const previousLiked = video.liked;
            const previousLikes = video.likes;
            video.liked = !video.liked;
            video.likes += video.liked ? 1 : -1;
            const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


            try {
                const res = await fetch(`/engagement/api/like/${video.id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,},
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

        follow() {
            
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
