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
                    const lastId = this.getHighestId();
                    tempListMessagesApi = listMessagesApi.replace('__CONVERSATION_ID__', conversationId)
                    const res = await fetch(`${tempListMessagesApi}?after_id=${lastId}`);
                    const data = await res.json();
                    if (data.results && data.results.length > 0) {
                        // Insert new messages at the top (since we have slice().reverse() in html template)
                        this.messagesList = [...data.results, ...this.messagesList];
                        this.scrollToBottom();
                    }
                } catch (e) {
                    console.error("Polling failed", e);
                }
            }, 5000); // poll every 5 seconds
        },

        getHighestId() {
            if (this.messagesList.length === 0) return 0;
            return Math.max(...this.messagesList.map(m => m.id));
        },

        async sendMessage() {
            if (!this.newMessage && !this.attachment) return;
            const formData = new FormData();
            if (this.newMessage) formData.append("content", this.newMessage);
            if (this.attachment) formData.append("attachment", this.attachment);

            try {
                const res = await fetch(sendMessageApi, {
                    method: "POST", body: formData
                });
                if (!res.ok) throw new Error("Failed to send message");

                const msg = await res.json();
                this.messagesList.unshift(msg); // flex-col-reverse
                this.newMessage = "";
                this.attachment = null;
                this.$refs.fileInput.value = null;
                this.scrollToBottom();
            } catch (e) {
                console.error("Send failed", e);
            }
        },

        handleFileUpload(event) {
            this.attachment = event.target.files[0];
        },

        scrollToBottom() {
            this.$nextTick(() => {
                const container = this.$refs.scrollContainer;
                container.scrollTop = container.scrollHeight;
                console.log(container.scrollHeight)
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
