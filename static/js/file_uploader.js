const upload_media = document.getElementById("upload_media");
const record_button = document.getElementById("record_button");
record_button.addEventListener("click", () => upload_media.click())

function fileUploader() {
    return {
        files: [],

        handleFiles(event) {
            const selectedFiles = Array.from(event.target.files);

            selectedFiles.forEach(file => {
                const fileData = {
                    file: file,
                    name: file.name,
                    type: file.type,
                    preview: URL.createObjectURL(file),
                    progress: 0,
                    description: ''
                };
                this.files.push(fileData);
            });

            event.target.value = '';
        },

        uploadFile(fileData) {
            const formData = new FormData();
            formData.append('file', fileData.file);
            formData.append('description', fileData.description);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/upload/"); // Replace with your Django endpoint

            xhr.upload.addEventListener("progress", (e) => {
                if (e.lengthComputable) {
                    fileData.progress = Math.round((e.loaded / e.total) * 100);
                }
            });

            xhr.onload = () => {
                if (xhr.status === 200) {
                    console.log('Upload success:', fileData.name);
                } else {
                    console.error('Upload failed:', fileData.name);
                }
            };

            xhr.onerror = () => console.error('Upload error:', fileData.name);

            xhr.send(formData);
        },

        uploadAllFiles() {
            this.files.forEach(file => {
                this.uploadFile(file);
            });
        }
    }
}