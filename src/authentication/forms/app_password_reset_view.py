from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy


class AppPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'

    def get_success_url(self):
        messages.success(self.request, 'Password reset instructions were sent to your email.')
        return reverse_lazy('login')
