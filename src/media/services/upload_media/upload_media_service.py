from django.core.files.uploadedfile import UploadedFile


class UploadMediaService:
    def upload(self, files: list[UploadedFile]) -> None:
        print(type(files)),
        # create trailer
        # send to queue
