function mediaFeed(feedType, mediaApiUrl, followUnfollowApi, createCommentApi, reportContentApi, likeMediaApi, listCommentsApi, filters) {
    return {
        mediaList: [],             // list of video objects
        page: 1,                   // pagination
        loadingMore: false,
        hasMore: true,
        currentIndex: 0,
        observer: null,
        progressBar: {},           // progress per index (0..100)
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
                const res = await fetch(`${mediaApiUrl}?page=${this.page}&type=${feedType}&filters=${filters}`);
                if (!res.ok) throw new Error('Failed to fetch media');
                const data = await res.json();

                // expected response shape: { results: [...], next_page: 2/null }
                const items = data.results || data;
                this.mediaList = this.mediaList.concat(items);
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

                    this.handleScroll()
                });
            }
        },

        handleScroll() {
            var $feed = $('#feed');
            var $containers = $feed.find('.media-container');
            var total = $containers.length;
            var index = 0;
            var isAnimating = false;
            var threshold = 50;
            var duration = 150; // animation duration in ms
            var touchStartY = 0;

            function goTo(targetIndex) {
                targetIndex = Math.max(0, Math.min(total - 1, targetIndex));
                if (isAnimating || targetIndex === index) return;

                isAnimating = true;
                index = targetIndex;

                var targetScroll = index * $containers.first().outerHeight();

                $feed.stop().animate(
                    {scrollTop: targetScroll},
                    duration,
                    'swing',
                    function () {
                        isAnimating = false;
                    }
                );
            }

            // --- Wheel / desktop ---
            $feed.on('wheel', function (e) {
                e.preventDefault();
                if (isAnimating) return;

                var delta = e.originalEvent.deltaY;
                if (delta > 0) goTo(index + 1);
                else if (delta < 0) goTo(index - 1);
            });

            // --- Touch / mobile ---
            $feed.on('touchstart', function (e) {
                touchStartY = e.originalEvent.touches[0].clientY;
            });

            $feed.on('touchend', function (e) {
                if (isAnimating) return;

                var touchEndY = e.originalEvent.changedTouches[0].clientY;
                var deltaY = touchStartY - touchEndY;

                if (Math.abs(deltaY) < threshold) return;

                if (deltaY > 0) goTo(index + 1);
                else goTo(index - 1);
            });

            // --- Resize ---
            $(window).on('resize', function () {
                $feed.scrollTop(index * $containers.first().outerHeight());
            });

            // Initial position
            $feed.scrollTop(0);
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
                    if (this.mediaList.length - index <= 5) {
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
            // pause all
            this.getMedia().forEach((media, i) => {
                const type = media.dataset.type;
                if (type === 'video') {
                    try {
                        if (i === index) {
                            // ensure we attempt to play; browsers require muted for autoplay
                            this.loadingVideo[i] = true;
                            media.play().then(() => {
                                this.loadingVideo[i] = false;
                            }).catch((e) => {
                                this.loadingVideo[i] = false;
                                console.log(e)
                            });
                            media.loop = true;
                        } else {
                            media.pause();
                            media.currentTime = 0; // optional: rewind off-screen videos
                            this.progressBar[i] = 0;
                        }
                    } catch (e) {
                        console.error(e);
                    }
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
            const previousLikes = media.like_count;
            media.liked = !media.liked;
            media.like_count += media.liked ? 1 : -1;

            try {
                tempLikeMediaApi = likeMediaApi.replace('__MEDIA_ID__', media.id)
                const res = await fetch(tempLikeMediaApi, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken(),},
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Like failed');
                // optionally update counts from server response
                const data = await res.json();
                if (data.like_count != null) media.like_count = data.like_count;
            } catch (e) {
                // rollback
                media.liked = previousLiked;
                media.like_count = previousLikes;
                console.error(e);
                alert('Failed to update like. Try again.');
            }
        },

        async follow_unfollow(media) {
            previousFollow = media.followed
            futureFollow = !media.followed

            try {
                this.mediaList.forEach(video => {
                    if (video.user.id === media.user.id) {
                        video.followed = futureFollow
                    }
                });

                const res = await fetch(followUnfollowApi, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken(),},
                    credentials: 'include',
                    body: JSON.stringify({'following': media.user.id})
                });

                if (!res.ok) throw new Error('Failed to follow performer.');
            } catch (e) {
                console.error(e);
                this.getMedia().forEach(video => {
                    if (video.user.id === media.user.id) {
                        video.followed = previousFollow
                    }
                });
                alert('Failed to follow performer.');
            } finally {
            }
        },

        async openComments(media) {
            this.commentsOpen = true;
            this.activeMedia = media;
            this.comments = [];
            this.commentInput = '';
            this.commentsLoading = true;

            try {
                tempListCommentsApi = listCommentsApi.replace('__MEDIA_ID__', media.id)
                const res = await fetch(tempListCommentsApi);
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
                const res = await fetch(createCommentApi, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken()},
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
            window.location.href = ` / user / $
                {
                    encodeURIComponent(user.username)
                }
                `;
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
                const res = await fetch(reportContentApi, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken(),},
                    body: JSON.stringify({'type': 'media', 'content_id': media.id}),
                    credentials: 'include'
                });
                if (!res.ok) throw new Error('Report failed');
                // optionally update counts from server response
                const data = await res.json();
                alert('Thanks for your feedback. We’ll review this video shortly.');
            } catch (e) {
                console.error(e);
            }
        },
    };
}
