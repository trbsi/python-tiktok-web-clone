'''
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import path, include

from src.authentication.forms.app_login_view import AppLoginView
from src.authentication.forms.app_password_reset_view import AppPasswordResetView

urlpatterns = [
    path('', include('src.core.urls')),
    path('admin/', admin.site.urls),
    path('authentication/', include('src.authentication.urls')),
    path('auth/login/', AppLoginView.as_view(), name='login'),
    path('auth/password_reset/', AppPasswordResetView.as_view(), name='password_reset'),
    path('auth/', include('django.contrib.auth.urls')),
    path('discover/', include('src.discover.urls')),
    path('feed/', include('src.feed.urls')),
    path('inbox/', include('src.inbox.urls')),
    path('user/', include('src.user.urls')),
    path('media/', include('src.media.urls')),
]
