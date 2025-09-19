from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AppLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('feed.following')
