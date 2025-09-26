from django.urls import reverse_lazy
from django.utils.http import urlencode


def reverse_lazy_with_query(route_name, kwargs=None, query_params=None):
    url = reverse_lazy(route_name, kwargs=kwargs)
    if query_params:
        url = url + f'?{urlencode(query_params)}'

    return url
