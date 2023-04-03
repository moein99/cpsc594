from django.contrib import admin
from django.urls import path

from app.views import Signup, Login

urlpatterns = [
    path("members/signup", Signup.as_view(), name="signup"),
    path("members/login", Login.as_view(), name="login"),
]
