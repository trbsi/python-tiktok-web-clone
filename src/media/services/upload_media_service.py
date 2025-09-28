import re as regex

from django.core.files.uploadedfile import UploadedFile

from src.media.models import Hashtag, Media


class UploadMediaService:
    def upload(self, files: list[UploadedFile]) -> None:


    def _handle_hashtags(self, description:str, media:Media) -> None:
        # r"#\w+" → '#' followed by one or more word characters (letters, digits, underscore)
        hashtags = regex.findall(r"#\w+", description)

        hashtags_ids=[]
        for hashtag in hashtags:
            record = Hashtag.objects.get_or_create(hashtag=hashtag)
            record.count += 1
            record.save()
            hashtags_ids.append(record.id)

        media.hashtags.add(hashtags_ids)