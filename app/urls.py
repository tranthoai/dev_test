from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("share", views.share_request, name="share"),
    path("movie/vote", views.vote_request, name="vote")
]
