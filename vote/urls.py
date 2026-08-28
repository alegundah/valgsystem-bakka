from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.VoteView.as_view(), name="vote"),
    path("login/", views.LoginForm.as_view(), name="login"),
    path("takk/", views.ThanksView.as_view(), name="thanks"),
    path("users/", views.UserView.as_view(), name="vote_users"),
]