import datetime
from gettext import ngettext

from django.db.models import Model
from django.urls import reverse_lazy
from django.utils.http import urlencode

from app import settings
from src.inbox.models import Conversation
from src.media.models import Media


def reverse_lazy_with_query(route_name, kwargs=None, query_params=None):
    url = reverse_lazy(route_name, kwargs=kwargs)
    if query_params:
        url = url + f'?{urlencode(query_params)}'

    return url


"""
# In general:
admin:appname_modelname_adminroute

# List (changelist)
reverse_lazy("admin:library_book_changelist")

# Add
reverse_lazy("admin:library_book_add")

# Change (needs object ID)
reverse_lazy("admin:library_book_change", args=[1])

# Delete
reverse_lazy("admin:library_book_delete", args=[1])

# History
reverse_lazy("admin:library_book_history", args=[1])
"""


def reverse_lazy_admin(object: Model, action: str, args: list = None):
    route = f'admin:{object._meta.app_label}_{object._meta.model_name}_{action}'
    return reverse_lazy(route, args=args)


def remote_file_path_for_conversation(conversation: Conversation, file_name: str) -> str:
    return f'conversation/{conversation.id}/{file_name}'


def remote_file_path_for_media(media: Media, file_name: str) -> str:
    return f'{media.file_type}/media/{media.id}/{file_name}'


def format_datetime(date: datetime):
    now = datetime.datetime.now(datetime.timezone.utc)
    # Ensure `dt` is timezone-aware
    if date.tzinfo is None:
        date = date.replace(tzinfo=datetime.timezone.utc)

    diff = now - date
    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = seconds // 3600
    days = diff.days

    if minutes < 60:
        return ngettext('%d minute ago', '%d minutes ago', minutes) % minutes
    elif hours < 24:
        return ngettext('%d hour ago', '%d hours ago', hours) % hours
    elif days < 7:
        return ngettext('%d day ago', '%d days ago', days) % days
    else:
        return date.strftime(settings.DATE_TIME_FORMAT)
