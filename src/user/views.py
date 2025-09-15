from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.user.services.delete_user.delete_user_service import DeleteUserService
from src.user.services.user_profile.user_profile_service import UserProfileService


@require_GET
def profile(request: HttpRequest, username: str) -> HttpResponse:
    user_profile_service = UserProfileService()
    user = user_profile_service.get_user(username)
    return render(request, 'profile.html', {
        'user': user,
        'logged_in_user': request.user
    })


@require_GET
def delete(request: HttpRequest) -> HttpResponse:
    return render(request, 'delete.html')


@require_POST
def do_delete(request: HttpRequest) -> HttpResponse:
    delete_user_service = DeleteUserService()
    delete_user_service.delete(user=request.user)
    logout(request)
    messages.success(request=request, message='Account deleted successfully')
    return redirect(reverse_lazy('home'))
