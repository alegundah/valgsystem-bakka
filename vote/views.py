from django.views import generic
from django.shortcuts import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.contrib.auth.models import Group

from .forms import LoginForm
from .models import *

# turn False to show statisticks
VOTING_ACTIVE = True

class LoginView(generic.View):
    template_name = "vote/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = (
            request.POST.get("username")
            or request.POST.get("code")
            or request.POST.get("password")
            or ""
        ).strip()

        user = User.objects.filter(username__iexact=code).first()

        if user:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("vote")

        return render(request, self.template_name, {"error": True})


class VoteView(LoginRequiredMixin, generic.View):
    def route_view(self):
        if not VOTING_ACTIVE:
            return StatsView
        if self.request.user.is_superuser:
            return GlobalVoteView

        vote, _ = Vote.objects.get_or_create(user=self.request.user)

        if vote.used():
            return None

        has_group = hasattr(self.request.user, "group") and self.request.user.group is not None

        if has_group and not vote.class_vote:
            return ClassVoteView
        elif not vote.global_vote:
            return GlobalVoteView

        return None

    def get(self, request):
        if not VOTING_ACTIVE:
            return redirect("stats")
        view = self.route_view()
        if view is None:
            return redirect("thanks")
        return view.as_view()(request)

    def post(self, request):
        if not VOTING_ACTIVE:
            return redirect("stats")
        view = self.route_view()
        if view is None:
            return redirect("thanks")
        return view.as_view()(request)


class GlobalVoteView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/kandidat.html"
    model = Candidate
    context_object_name = "candidates"
    extra_context = {"vote_type": "globalt"}
    
    def post(self, request):
        candidate = request.POST["candidate"]
        vote: Vote = request.user.vote
        vote.global_vote = get_object_or_404(Candidate, id=candidate)
        vote.save()
        return redirect(resolve_url("thanks"))


class ClassVoteView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/kandidat.html"
    context_object_name = "candidates"
    extra_context = {"vote_type": "lokalt"}

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


class StatsView(LoginRequiredMixin, generic.View):
    def get(self, request):
        selected_group = request.GET.get("group", "Global")
        groups = ["Global"] + list(Group.objects.values_list("name", flat=True))

        candidates = Candidate.objects.all()
        if selected_group != "Global":
            candidates = candidates.filter(class_name__name=selected_group)

        candidate_data = []
        max_votes = 1

        for c in candidates:
            v_count = Vote.objects.filter(Q(global_vote=c) | Q(class_vote=c)).count()
            if v_count > max_votes:
                max_votes = v_count
            candidate_data.append({
                "candidate": c,
                "votes": v_count,
            })

        candidate_data.sort(key=lambda x: x["votes"], reverse=True)

        for item in candidate_data:
            item["bar_percentage"] = int((item["votes"] / max_votes) * 100) if max_votes > 0 else 0

        return render(request, "vote/statistikk.html", {
            "groups": groups,
            "selected_group": selected_group,
            "candidates": candidate_data,
        })


class UserView(LoginRequiredMixin, generic.ListView):
    template_name = "vote/users.html"

    def get(self, request):
        u: User = request.user
        if not u.is_superuser: 
            return self.handle_no_permission()
        g: Group = get_list_or_404(Group)
        return render(request, self.template_name, {"groups": g})

    def handle_no_permission(self):
        return redirect(resolve_url("/admin/"))

    def post(self, request):
        delete_users()
        classes = get_list_or_404(Group)
        for c in classes:
            for i in range(25):
                create_user(c)
        return redirect(resolve_url("vote_users"))