from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


class AppPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'

    def get_success_url(self):
        messages.success(self.request, 'Your password was successfully updated!')
        return reverse_lazy('user.profile', kwargs={'username': self.request.user.username})
