function userSuggestionComponent(userSuggestionApi, updateDescriptionCallback) {
    return {
        openUserSuggestion: false,
        suggestions: [],
        highlightedIndex: 0,
        lastAtIndex: -1,

        async fetchSuggestions(event) {
            let query = event.value
            const cursor = event.selectionStart;

             // find the last "@" before the cursor
            this.lastAtIndex = query.lastIndexOf("@", cursor - 1);
            if (this.lastAtIndex === -1) {
                this.openUserSuggestion = false;
                return;
            }

            // extract the query after "@"
            query = query.substring(this.lastAtIndex + 1, cursor);

            // stop if query contains invalid characters
            if (!query.match(/^[a-zA-Z0-9]*$/)) {
                this.openUserSuggestion = false;
                return;
            }

            // require at least 3 characters
            if (query.length < 3) {
                this.openUserSuggestion = false;
                return;
            }

            try {
                const res = await fetch(`${userSuggestionApi}?query=${encodeURIComponent(query)}`);
                this.suggestions = await res.json();
                this.highlightedIndex = 0;
                this.openUserSuggestion = this.suggestions.length > 0;
            } catch (err) {
                console.error("Error fetching suggestions:", err);
                this.suggestions = [];
                this.openUserSuggestion = false;
            }
        },

        chooseUsername(username, index) {
            // get textarea by id
            const textarea = document.getElementById("description_field_"+index);
            if (!textarea) return;

            const cursor = textarea.selectionStart;
            var textValue = textarea.value;

            const lastAtIndex = textValue.lastIndexOf("@", cursor - 1);
            if (lastAtIndex === -1) return;

            const beforeAt = textValue.substring(0, lastAtIndex);
            const afterCursor = textValue.substring(cursor);

            // insert chosen username
            textValue = `${beforeAt}@${username} ${afterCursor}`;

            // move cursor after inserted username
            const newCursorPos = beforeAt.length + username.length + 2;
            textarea.setSelectionRange(newCursorPos, newCursorPos);

            this.openUserSuggestion = false;
            updateDescriptionCallback(index, textValue);
        },

        selectNext() {
            if (!this.openUserSuggestion) return;
            this.highlightedIndex =
                (this.highlightedIndex + 1) % this.suggestions.length;
        },

        selectPrev() {
            if (!this.openUserSuggestion) return;
            this.highlightedIndex =
                (this.highlightedIndex - 1 + this.suggestions.length) % this.suggestions.length;
        }
    };
}
