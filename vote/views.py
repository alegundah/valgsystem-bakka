from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return render(self.request, self.template_name, {"error": True})
            
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"error": True})


class VoteView(LoginRequiredMixin, generic.View):
    def route_view(self):
        vote: Vote = self.request.user.vote
        if vote.used():
            return None
        elif not vote.class_vote:
            return ClassVoteView
        elif not vote.global_vote:
            return GlobalVoteView
        return None

    def get(self, request):
        view = self.route_view()
        if view is None:
            return redirect("thanks")
        return view.as_view()(request)

    def post(self, request):
        view = self.route_view()
        if view is None:
            return redirect("thanks")
        return view.as_view()(request)

class GlobalVoteView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/kandidat.html"
    model = Candidate
    context_object_name = "candidates"
    
    def post(self, request):
        candidate = request.POST["candidate"]
        vote: Vote = request.user.vote
        vote.global_vote = Candidate.objects.get(id=candidate)
        vote.save()
        return redirect(reverse("thanks"))

class ClassVoteView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/kandidat.html"
    context_object_name = "candidates"

    def get_queryset(self):
        class_name = self.request.user.class_name
        return Candidate.objects.filter(class_name=class_name)

    
    def post(self, request):
        candidate = request.POST["candidate"]
        vote: Vote = request.user.vote
        vote.class_vote = Candidate.objects.get(id=candidate)
        vote.save()
        return redirect(reverse("vote"))

class ThanksView(generic.TemplateView):
    template_name = "vote/thanks.html"

class UserView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/users.html"
    model = Group
    context_object_name = "groups"

    def post(self, request):
        delete_users()
        classes = Group.objects.all()
        for c in classes:
            for i in range(20):
                create_user(c)
        return HttpResponseRedirect(reverse("vote_users"))