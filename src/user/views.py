from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.user.forms.update_email_form import UpdateEmailForm
from src.user.forms.update_profile_form import UpdateProfileForm
from src.user.models import User
from src.user.services.change_email.email_change_service import EmailChangeService
from src.user.services.delete_user.delete_user_service import DeleteUserService
from src.user.services.user_following.user_following_service import UserFollowingService
from src.user.services.user_media.user_media_service import UserMediaService
from src.user.services.user_profile.user_profile_service import UserProfileService


# ------------------- USER PROFILE HOMEPAGE ------------------------
@require_GET
def profile(request: HttpRequest, username: str) -> HttpResponse:
    logged_in_user = request.user
    user_profile_service = UserProfileService()
    current_user: User = user_profile_service.get_user_by_username(username)

    if current_user.is_regular_user() and current_user.username != logged_in_user.username:
        raise Http404

    if current_user.is_performer():
        media_api_url = reverse_lazy('user.api.get_media')
    else:
        media_api_url = reverse_lazy('user.api.get_following')

    return render(request, 'profile.html', {
        'current_user': current_user,
        'logged_in_user': logged_in_user,
        'media_api_url': media_api_url
    })


@require_GET
def api_get_user_media(request: HttpRequest) -> JsonResponse:
    get = request.GET
    page = int(get.get('page'))
    username = get.get('username')
    user_media_service = UserMediaService()
    data: dict = user_media_service.get_user_media(username=username, current_page=page)

    return JsonResponse({'results': data['result'], 'next_page': data['next_page']})


@require_GET
@login_required
def api_get_following(request: HttpRequest) -> JsonResponse:
    get = request.GET
    page = int(get.get('page'))
    service = UserFollowingService()
    result = service.get_following(user=request.user, current_page=page)

    return JsonResponse({'results': result['result'], 'next_page': result['next_page']})


# ------------------- UPDATE PROFILE ------------------------
def update_profile(request: HttpRequest) -> HttpResponse:
    form = UpdateProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        # TODO move to service
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            form.resize_image()
            return redirect('user.profile', username=request.user.username)

    return render(
        request,
        'update_profile.html',
        {'form': form, 'user': request.user}
    )


# ------------------- USER LIKED MEDIA ------------------------
@require_GET
@login_required
def profile_liked_media(request: HttpRequest, username: str) -> HttpResponse:
    user = request.user
    if user.username != username:
        raise Http404

    user_profile_service = UserProfileService()
    user = user_profile_service.get_user_by_username(username=username)

    return render(request, 'profile.html', {
        'current_user': user,
        'logged_in_user': request.user,
        'media_api_url': reverse_lazy('user.api.get_liked_media')
    })


@require_GET
@login_required
def api_get_user_liked_media(request: HttpRequest) -> JsonResponse:
    get = request.GET
    user_media_service = UserMediaService()
    data: dict = user_media_service.get_user_liked_media(
        username=get.get('username'),
        current_page=int(get.get('page'))
    )

    return JsonResponse({'results': data['result'], 'next_page': data['next_page']})


# ------------------- DELETE USER ------------------------
@require_GET
@login_required
def delete(request: HttpRequest) -> HttpResponse:
    return render(request, 'delete.html')


@require_POST
@login_required
def do_delete(request: HttpRequest) -> HttpResponse:
    delete_user_service = DeleteUserService()
    delete_user_service.delete(user=request.user)
    logout(request)
    messages.success(request=request, message='Account deleted successfully')
    return redirect(reverse_lazy('home'))


# ------------------- UPDATE EMAIL ------------------------
@login_required
def update_email(request: HttpRequest) -> HttpResponse:
    form = UpdateEmailForm(initial={'email': request.user.email})
    if request.method == 'POST':
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            service = EmailChangeService()
            service.request_email_change(request=request, user=request.user, new_email=email)
            messages.success(request=request, message='Confirmation email has been sent.')
            return redirect(reverse_lazy('user.update_email'))

    return render(request, 'update_email.html', {'form': form})


@require_GET
def confirm_email_change(request, token):
    service = EmailChangeService()
    change = service.get_email_change(token=token)

    if change.is_expired():
        messages.success(request=request, message='Email changed token expired')
        return redirect('user.update_email')

    service.change_email(change=change)
    messages.success(request=request, message='Email changed successfully')
    return redirect('user.update_email')
