from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class AppLoginView(LoginView):
    template_name = 'login.html'
