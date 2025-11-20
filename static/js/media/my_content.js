function myContentComponent(userSuggestionApi) {
    return {
        descriptions: [],
        userSuggestionComponent: null,
        init() {
            this.userSuggestionComponent = userSuggestionComponent(
                userSuggestionApi,
                (fileId, descriptionValue) => {
                    document.getElementById('description_field_' + fileId).value = descriptionValue;
                },
            )
        },
    }
}