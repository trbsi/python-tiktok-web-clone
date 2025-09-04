from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AppLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        messages.success(self.request, 'You can log in now')
        return reverse_lazy('feed.home')
