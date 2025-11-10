from src.inbox.models import Conversation
from src.media.models import Media


def remote_file_path_for_conversation(conversation: Conversation, file_name: str) -> str:
    return f'conversation/{conversation.id}/{file_name}'


def remote_file_path_for_media(media: Media, file_name: str) -> str:
    return f'{media.file_type}/media/{media.user_id}/{file_name}'
