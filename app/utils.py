import datetime
from gettext import ngettext

from django.urls import reverse_lazy
from django.utils.http import urlencode

from app import settings


def reverse_lazy_with_query(route_name, kwargs=None, query_params=None):
    url = reverse_lazy(route_name, kwargs=kwargs)
    if query_params:
        url = url + f'?{urlencode(query_params)}'

    return url


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
