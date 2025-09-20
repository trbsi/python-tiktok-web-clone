from django.urls import path

from . import views

urlpatterns = [
    path('conversations', views.list_conversations, name='inbox.conversations'),
    path('messages/<str:username>', views.list_messages, name='inbox.messages'),
    path('send-message', views.send_message, name='inbox.send_message'),
    path('api/delete', views.api_delete, name='inbox.api.delete'),
    path('api/list-conversations', views.api_list_conversations, name='inbox.api.list_conversations'),
    path('api/list-messages', views.api_list_messages, name='inbox.api.list_messages'),
    path('api/send-message', views.api_send_message, name='inbox.api.send_message'),
    path('api/polling-messages', views.api_polling_messages, name='inbox.api.polling_messages'),
]
