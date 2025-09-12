from django.db import models
from django.db.models import QuerySet

from src.user.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_relations', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_relations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('follower', 'following'), name='unique_follower')
        ]

    @staticmethod
    def get_followers(user) -> QuerySet[User]:
        """
        Returns all users who follow the given user.
        """
        return User.objects.filter(following_relations__following=user)

    @staticmethod
    def get_following(user) -> QuerySet[User]:
        """
        Returns all users that the given user is following.
        """
        return User.objects.filter(follower_relations__follower=user)

    @staticmethod
    def is_follower(user_a: int, user_b: int) -> bool:
        """
        Returns True if user_a is a follower of user_b.
        Example: Follow.is_follower(alice, bob) -> True if Alice follows Bob
        """
        return Follow.objects.filter(follower=user_a, following=user_b).exists()

    @staticmethod
    def is_following(user_a: int, user_b: int) -> bool:
        """
        Returns True if user_a is following user_b.
        Example: Follow.is_following(alice, bob) -> True if Alice follows Bob
        """
        return Follow.objects.filter(follower=user_a, following=user_b).exists()
