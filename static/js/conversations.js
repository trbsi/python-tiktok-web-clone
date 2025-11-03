function conversationsComponent(listConversationsApi, deleteConversationApi) {
    return {
        conversationsList: [], page: 1, loading: false, allLoaded: false, selectedIds: [],

        async loadMore() {
            if (this.loading || this.allLoaded) return;
            this.loading = true;

            try {
                const response = await fetch(`${listConversationsApi}?page=${this.page}`);
                if (!response.ok) throw new Error("Failed to fetch conversations");

                const data = await response.json();
                if (data.results && data.results.length > 0) {
                    this.conversationsList.push(...data.results);
                    this.page = data.next_page;
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

        toggleSelection(conversationId, checked) {
            if (checked) {
                this.selectedIds.push(conversationId);
            } else {
                this.selectedIds = this.selectedIds.filter(x => x !== conversationId);
            }
        },

        async deleteSelected() {
            if (this.selectedIds.length === 0) return;

            try {
                // Send delete request to API
                const response = await fetch(deleteConversationApi, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.$utils.getCsrfToken()
                    },
                    body: JSON.stringify({conversation_ids: this.selectedIds})
                });

                if (!response.ok) throw new Error("Failed to delete conversations");

                // Remove deleted items from UI
                this.conversationsList = this.conversationsList.filter(conversation => !this.selectedIds.includes(conversation.id));
                this.selectedIds = [];
            } catch (error) {
                console.error(error);
            }
        },

        handleScroll(event) {
            const el = event.target;
            if (el.scrollTop + el.clientHeight >= el.scrollHeight - 50) {
                this.loadMore();
            }
        }
    };
}

$('#auto_reply_messages').change(function() {
    var value = $(this).is(':checked');
    toggleAutoReply(value);
});

async function toggleAutoReply(isChecked) {
    const response = await fetch(toggle_auto_reply_api, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken()
        },
        body: JSON.stringify({auto_reply_active: isChecked})
    });
}