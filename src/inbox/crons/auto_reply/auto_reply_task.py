from src.inbox.models import Message, Conversation
from src.inbox.services.inbox_settings.inbox_settings_service import InboxSettingsService


class AutoReplyTask:
    def auto_reply(self, message_id: int):
        inbox_settings_service = InboxSettingsService()
        message: Message = Message.objects.get(id=message_id)

        # if creator sent a message do not auto reply
        if message.sender.is_creator():
            return

        conversation: Conversation = message.conversation
        creator = conversation.get_creator()

        auto_reply_active = inbox_settings_service.is_auto_reply_active(user=creator)
        if auto_reply_active == False:
            return

        # @TODO auto reply
