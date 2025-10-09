from decimal import Decimal

from src.engagement.models import Comment
from src.inbox.models import Message
from src.media.models import Media
from src.payment.models import Balance, Spending
from src.user.models import User


class SpendService:
    COMMENT_COINS = 20  # 0.2$
    VIDEO_COINS = 100  # 1$
    IMAGE_COINS = 50  # 0.5$
    TEXT_MESSAGE_COINS = 10  # 0.1$
    MEDIA_MESSAGE_COINS = 100  # 1$

    def comment(self, user: User, comment: Comment) -> Decimal:
        return self._spend(spender=user, recipient=comment.media.user.id, amount=Decimal(self.COMMENT_COINS),
                           object=comment)

    def media_unlock(self, user: User, media: Media) -> Decimal:
        if media.is_image():
            amount = self.IMAGE_COINS
        elif media.is_video():
            amount = self.VIDEO_COINS

        return self._spend(spender=user, recipient=media.user.id, amount=Decimal(amount), object=media)

    def message(self, user: User, message: Message) -> Decimal:
        if message.is_media_message():
            amount = self.MEDIA_MESSAGE_COINS
        else:
            amount = self.TEXT_MESSAGE_COINS

        return self._spend(spender=user, recipient=message.conversation.get_creator(), amount=Decimal(amount),
                           object=message)

    def _spend(
            self,
            spender: User,
            recipient: User,
            amount: Decimal,
            object: Message | Media | Comment
    ) -> Decimal:
        if spender.is_creator():
            return

        spender_balance = Balance.objects.get(user=spender)
        recipient_balance = Balance.objects.get(user=recipient)

        if spender_balance.balance < amount:
            raise Exception('Balance too low')

        spender_balance.balance = spender_balance.balance - amount
        spender_balance.save()

        recipient_balance = recipient_balance.balance + amount
        recipient_balance.save()

        Spending.objects.create(
            by_user=spender,
            on_user=recipient_balance,
            amount=amount,
            content_object=object
        )

        return amount
