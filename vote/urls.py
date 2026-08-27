from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.VoteView.as_view(), name="vote"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("takk/", views.ThanksView.as_view(), name="thanks"),
    path("brukere/", views.UserView.as_view(), name="vote_users"),
    path("statistikk/", views.StatsView.as_view(), name="stats"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]