from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.register_request, name="register"),
    path("register", views.register_request, name="register")
]