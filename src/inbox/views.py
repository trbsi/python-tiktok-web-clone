import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.inbox.services.delete_conversation.delete_conversation_service import DeleteConversationService
from src.inbox.services.list_conversations.list_conversations_service import ListConversationsService
from src.inbox.services.list_messages.can_user_access_conversation_specification import \
    CanUserAccessConversationSpecification
from src.inbox.services.list_messages.list_messages_service import ListMessagesService
from src.inbox.services.list_messages.read_messages_service import ReadConversationService


# --------------------------------- CONVERSATIONS -------------------------------
@require_GET
@login_required
def list_conversations(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'inbox_conversations.html',
        {
            'list_conversations_api': reverse_lazy('inbox.api.list_conversations'),
            'delete_conversation_api': reverse_lazy('inbox.api.delete'),
        }
    )


@require_GET
@login_required
def api_list_conversations(request: HttpRequest) -> JsonResponse:
    get = request.GET
    service = ListConversationsService()
    data = service.list_conversations(current_user=request.user, current_page=get.get('page'))

    return JsonResponse({'results': data['result'], 'next_page': data['next_page']})


@require_POST
@login_required
def api_delete(request: HttpRequest) -> JsonResponse:
    post = json.loads(request.body)
    service = DeleteConversationService()
    service.delete_conversations(ids=post['conversation_ids'], current_user=request.user)
    return JsonResponse({})


# --------------------------------- MESSAGES -------------------------------
@require_GET
@login_required
def list_messages(request: HttpRequest, conversation_id: int) -> HttpResponse:
    user = request.user
    specification = CanUserAccessConversationSpecification()
    result = specification.check(conversation_id=conversation_id, user=user)
    if not result:
        raise Http404

    read_service = ReadConversationService()
    conversation = read_service.read_conversation(conversation_id=conversation_id, user=user)
    other_user = conversation.get_other_user(current_user=user)

    return render(
        request,
        'inbox_messages.html',
        {
            'other_user': other_user,
            'current_user_id': user.id,
            'conversation_id': conversation_id,
            'list_messages_api': reverse_lazy('inbox.api.list_messages',
                                              kwargs={'conversation_id': '__CONVERSATION_ID__'}),
            'send_message_api': reverse_lazy('inbox.api.send_message'),
        }
    )


@require_GET
@login_required
def api_list_messages(request: HttpRequest, conversation_id: int) -> JsonResponse:
    get = request.GET
    after_id = get.get('after_id')
    page = int(get.get('page'))
    user = request.user

    specification = CanUserAccessConversationSpecification()
    result = specification.check(conversation_id=conversation_id, user=user)
    if not result:
        raise Http404

    service = ListMessagesService()
    result = service.list_messages(conversation_id=conversation_id, current_page=page, after_id=after_id)

    return JsonResponse({'results': result['result'], 'next_page': result['next_page']})


# GET and POST
@login_required
def send_message(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_message.html')


@require_POST
@login_required
def api_send_message(request: HttpRequest) -> JsonResponse:
    return render(request, 'inbox_messages.html')
