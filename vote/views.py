from django.views import generic
from django.shortcuts import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm
from .models import *

class LoginForm(generic.FormView):
    template_name = "vote/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("vote")

    def form_valid(self, form):
        try:
            user = get_object_or_404(User, username=form.cleaned_data["username"])
        except User.DoesNotExist:
            return render(self.request, self.template_name, {"error": True})    
        login(self.request, user)

        return redirect(resolve_url("vote"))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"error": True})


class VoteView(LoginRequiredMixin, generic.View):
    def route_view(self):
        if self.request.user.is_superuser:
            return GlobalVoteView
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
        vote.global_vote = get_object_or_404(Candidate, id=candidate)
        vote.save()
        return redirect(resolve_url("thanks"))

class ClassVoteView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/kandidat.html"
    context_object_name = "candidates"

    def get_queryset(self):
        class_name = self.request.user.class_name
        return get_list_or_404(Candidate, class_name=class_name)

    
    def post(self, request):
        candidate = request.POST["candidate"]
        vote: Vote = request.user.vote
        vote.class_vote = get_object_or_404(Candidate, id=candidate)
        vote.save()
        return redirect(resolve_url("vote"))

class ThanksView(generic.TemplateView):
    template_name = "vote/thanks.html"

class UserView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/users.html"

    def get(self, request):
        u: User = request.user
        if not u.is_superuser: 
            return self.handle_no_permission()
        g: Group = get_list_or_404(Group)
        return render(request, self.template_name, {"groups": g})

    def handle_no_permission(self):
        return redirect("admin")

    def post(self, request):
        delete_users()
        classes = get_list_or_404(Group)
        for c in classes:
            for i in range(25):
                create_user(c)
        return redirect(resolve_url("vote_users"))
