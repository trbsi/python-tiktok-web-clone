from django.core.paginator import Paginator

from app import settings
from src.inbox.models import Message


class ListMessagesService:
    PER_PAGE = 25
    PER_PAGE_AFTER_ID = 100

    def list_messages(self, conversation_id: int, current_page: int, after_id: int | None) -> dict:
        messages = (
            Message.objects
            .filter(conversation_id=conversation_id)
            .select_related('sender')
            .order_by('-id')
        )
        per_page = self.PER_PAGE

        if after_id is not None:
            current_page = 1
            per_page = self.PER_PAGE_AFTER_ID
            messages = messages.filter(id__gt=after_id)

        paginator = Paginator(object_list=messages, per_page=per_page)
        page = paginator.page(current_page)

        result = []
        for message in page.object_list:
            result.append(
                {
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
            )

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
