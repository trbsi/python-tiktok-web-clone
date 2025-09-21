from app import settings
from src.inbox.models import Message
from src.user.models import User


class SendMessageService:
    def send_message(
            self,
            user: User,
            conversation_id: int,
            messageContent: str | None
    ) -> dict:
        message = Message.objects.create(sender=user, conversation_id=conversation_id, message=messageContent)
        # TODO upload attachment and save

        return {
            'id': message.id,
            'created_at': message.created_at.strftime(settings.DATE_TIME_FORMAT),
            'message': message.message,
            'attachment_url': message.attachment_url,
            'sender': {
                'id': message.sender.id,
                'profile_picture': message.sender.get_profile_picture(),
                'username': message.sender.username,
            }
        }
