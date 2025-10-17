from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .register_form import RegisterForm


class RegisterFormView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_form_kwargs(self):
        """
        Add `request` to form kwargs so the form can access it.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form: RegisterForm):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'You can logs in now')
        return reverse_lazy('login')
