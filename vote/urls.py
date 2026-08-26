from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.index, name="vote"),
    path("login/", views.LoginForm.as_view(), name="login"),
    path("takk/", views.ThankView.as_view(), name="thanks")
]