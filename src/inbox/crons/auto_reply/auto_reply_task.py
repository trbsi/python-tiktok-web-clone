import torch

from src.inbox.models import Message, Conversation
from src.inbox.services.inbox_settings.inbox_settings_service import InboxSettingsService


class AutoReplyTask:
    def __init__(
            self,
            tokenizer,
            model,
            inbox_settings_service: InboxSettingsService | None = None,
    ):
        # @TODO
        print(type(tokenizer))
        print(type(model))
        self.tokenizer = tokenizer
        self.model = model
        self.inbox_settings_service = inbox_settings_service or InboxSettingsService()

    def auto_reply(self, message_id: int, send_message_service):
        message: Message = Message.objects.get(id=message_id)

        # if creator sent a message do not auto reply
        if message.sender.is_creator():
            return

        conversation: Conversation = message.conversation
        creator = conversation.get_creator()

        auto_reply_active = self.inbox_settings_service.is_auto_reply_active(user=creator)
        if auto_reply_active == False:
            return

        # Get last 100 messages as context
        last_messages = (
            Message.objects
            .select_related('sender')
            .filter(conversation=conversation)
            .filter(id__lte=message_id)
            .order_by('-id')[:100]
        )
        last_messages = last_messages.reverse()

        # Create GPT format
        history = []
        for message in last_messages:
            if message.sender.is_creator():
                prefix = 'Bot: '
            else:
                prefix = 'User: '
            history.append(prefix + message.message)
        history.append('Bot: ')
        textual_history = '\n'.join(history)

        # Get reply and save
        reply = self._get_reply(textual_history)
        send_message_service.send_message(
            user=creator,
            conversation_id=conversation.id,
            message_content=reply,
        )

    def _get_reply(self, textual_history) -> str:
        inputs = self.tokenizer.encode(textual_history, return_tensors='pt')
        if torch.cuda.is_available():
            self.model.to('cuda')
            inputs = inputs.to('cuda')

        reply_ids = self.model.generate(inputs=inputs, max_length=128, pad_token_id=self.tokenizer.eos_token_id)

        return self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)
