function chatComponent(listMessagesApi, sendMessageApi, conversationId, currentUserId) {
    return {
        messagesList: [],
        nextPage: 1,
        loading: false,
        pollingInterval: null,
        newMessage: "",
        attachment: null,
        allLoaded: false,
        currentUserId: currentUserId,
        isSending: false,
        highestMessageId: null,
        previewUrl: null,

        async initChat() {
            await this.loadMessages();
            this.scrollToBottom();
            this.startPolling();
        },

        async loadMessages() {
            if (this.loading || this.allLoaded) return;
            this.loading = true;

            try {
                tempListMessagesApi = listMessagesApi.replace('__CONVERSATION_ID__', conversationId)
                const response = await fetch(`${tempListMessagesApi}?page=${this.nextPage}`);
                if (!response.ok) throw new Error("Failed to fetch messages");

                const data = await response.json();
                if (data.results && data.results.length > 0) {
                    // Add older messages to the bottom (flex-col-reverse means "append")
                    this.messagesList.push(...data.results);
                    this.nextPage = data.next_page;
                    if (!data.next_page) this.allLoaded = true;
                } else {
                    this.allLoaded = true;
                }
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },


        handleScroll(event) {
            const el = event.target;
            if (el.scrollTop < 50 && this.nextPage) {
                this.loadMessages();
            }
        },

        startPolling() {
            this.pollingInterval = setInterval(async () => {
                try {
                    const lastId = this.getHighestId(); // highest message ID we have
                    const tempListMessagesApi = listMessagesApi.replace('__CONVERSATION_ID__', conversationId);
                    const res = await fetch(`${tempListMessagesApi}?after_id=${lastId}`);
                    const data = await res.json();

                    if (data.results && data.results.length > 0) {
                        data.results.forEach(newMessage => {
                            const index = this.messagesList.findIndex(msg => msg.id === newMessage.id);

                            if (index !== -1) {
                                // Replace the existing message
                                this.messagesList.splice(index, 1, newMessage);
                            } else {
                                // Add as a new message at the bottom
                                this.messagesList.push(newMessage);
                            }
                        });

                        this.scrollToBottom();
                        this.highestMessageId = null;
                    }
                } catch (e) {
                    console.error("Polling failed", e);
                }
            }, 5000); // poll every 5 seconds
        },

        getHighestId() {
            if (this.highestMessageId !== null) {
                return this.highestMessageId;
            }

            if (this.messagesList.length === 0) {
                return 0;
            }
            return Math.max(...this.messagesList.map(message => message.id));
        },

        async sendMessage() {
            if (!this.newMessage && !this.attachment) return;

            if (this.attachment) {
                type = 'media_message';
            } else {
                type = 'text_message'
            }
            result = await canSpend(type);
            if (result['ok'] === false) {
                return;
            }

            // Set isSending state to true
            this.isSending = (this.attachment !== null) ? true : false;

            // Prepare FormData
            const formData = new FormData();
            formData.append('conversationId', conversationId);
            if (this.newMessage) formData.append("message", this.newMessage);
            if (this.attachment) formData.append("attachment", this.attachment);

            try {
                const res = await fetch(sendMessageApi, {
                    method: "POST",
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Accept': 'application/json'
                    }
                });
                if (!res.ok) throw new Error("Failed to send message");

                const msg = await res.json();
                this.messagesList.push(msg); // add message to list

                if (this.attachment !== null) {
                    this.highestMessageId = msg.id - 1
                }

                // Reset input
                this.newMessage = "";
                this.$refs.messageInput.style.height = "auto"; // reset textarea
                this.removeAttachment()

                this.scrollToBottom();
            } catch (e) {
                console.error("Send failed", e);
            } finally {
                this.isSending = false; // hide loader
            }
        },

        isAttachmentImage() {
            return this.attachment && this.attachment.type.startsWith('image/');
        },

        isAttachmentVideo() {
            return this.attachment && this.attachment.type.startsWith('video/');
        },

        handleFileUpload(event) {
            if (event.target.files.length > 0) {
                this.attachment = event.target.files[0];
                if (!this.attachment.type.startsWith('video/') && !this.attachment.type.startsWith('image/')) {
                    this.attachment = null;
                    return;
                }
                this.previewUrl = URL.createObjectURL(this.attachment);
            }
        },

        removeAttachment() {
            this.attachment = null;
            this.previewUrl && URL.revokeObjectURL(this.previewUrl);
            this.previewUrl = null;
            this.$refs.fileInput.value = null; // reset input so the same file can be chosen again
        },

        scrollToBottom() {
            this.$nextTick(() => {
                const container = this.$refs.scrollContainer;
                container.scrollTop = container.scrollHeight;
            });
        },

        isImage(url) {
            return url.match(/\.(jpeg|jpg|gif|png|webp)$/i);
        },

        isVideo(url) {
            return url.match(/\.(mp4|mov|webm|ogg)$/i);
        },

        formatTime(dateStr) {
            return dateStr;
        }
    };
}