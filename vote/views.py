from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from .models import *

class LoginForm(generic.FormView):
    template_name = "vote/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("vote")

    def form_valid(self, form):
        try:
            user = User.objects.get(username=form.cleaned_data["username"])
        except User.DoesNotExist:
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


@login_required
def index(request):
    return render(request, "vote/kandidat.html")