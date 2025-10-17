function fileUploader(uploadApi) {
    return {
        files: [],           // all files in the UI (including uploaded)
        uploadedFiles: [],   // track files already uploaded

        handleFiles(event) {
            const selectedFiles = Array.from(event.target.files);

            selectedFiles.forEach(file => {
                // skip files that are already uploaded
                if (this.uploadedFiles.some(f => f.name === file.name && f.size === file.size)) return;

                const fileData = {
                    file: file,
                    name: file.name,
                    size: file.size,
                    type: file.type,
                    preview: URL.createObjectURL(file),
                    progress: 0,
                    description: '',
                    status: 'pending',          // pending | uploading | finalizing | completed | failed
                    statusMessage: ''
                };
                this.files.push(fileData);
            });

            event.target.value = '';
        },

        uploadFile(fileData, postType) {
            // skip if already uploaded
            if (fileData.status === 'completed') return;

            fileData.status = 'uploading';
            fileData.statusMessage = 'Uploading…';

            const formData = new FormData();
            formData.append('postType', postType);
            formData.append('file', fileData.file);
            formData.append('description', fileData.description);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", uploadApi);
            xhr.setRequestHeader("X-CSRFToken", this.$utils.getCsrfToken());

            xhr.upload.addEventListener("progress", (e) => {
                if (e.lengthComputable) {
                    fileData.progress = Math.round((e.loaded / e.total) * 100);
                    if (fileData.progress === 100) {
                        fileData.statusMessage = "Finalizing upload…";
                        fileData.status = 'finalizing';
                    }
                }
            });

            xhr.onload = () => {
                if (xhr.status === 200) {
                    fileData.statusMessage = "Upload complete ✅";
                    fileData.status = 'completed';

                    // add to uploadedFiles array to prevent re-upload
                    if (!this.uploadedFiles.includes(fileData)) {
                        this.uploadedFiles.push(fileData);
                    }
                } else {
                    fileData.statusMessage = "Upload failed ❌";
                    fileData.status = 'failed';
                }
            };

            xhr.onerror = () => {
                fileData.statusMessage = "Upload error ❌";
                fileData.status = 'failed';
            };

            xhr.send(formData);
        },

        uploadAllFiles(postType) {
            this.files.forEach(file => {
                if (file.status !== 'completed') {
                    this.uploadFile(file, postType);
                }
            });
        }
    }
}
