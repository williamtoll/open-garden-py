from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers

urlpatterns = [
    path("SignIn", views.SignIn.as_view(), name="SignIn"),
    path("Register", views.Register.as_view(), name="Register"),
]
