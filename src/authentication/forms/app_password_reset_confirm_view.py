from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class AppPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Your password was successfully updated!')
        return reverse_lazy('login')
