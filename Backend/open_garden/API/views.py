from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, action
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
import json
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, status, viewsets, permissions
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from .models import *
import base64
from django.utils.html import escape
import ast
from django.contrib.auth.models import User


from rest_framework.authtoken.views import APIView
from rest_framework.response import Response


from rest_framework import viewsets
from rest_framework import response

# SignIn Route


class SignIn(generics.GenericAPIView):
    def post(self, request):
        Username = request.data["Username"]
        Password = request.data["Password"]
        user = authenticate(request, username=Username, password=Password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            response = {
                "Name": user.first_name + user.last_name,
                "Email": user.email,
                "Username": user.username,
                "Token": token.key,
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                "Invalid Credentials", status=status.HTTP_400_BAD_REQUEST, safe=False
            )


class Register(generics.GenericAPIView):
    def post(self, request):
        First_Name = request.data["First_Name"]
        Last_Name = request.data["Last_Name"]
        Username = request.data["Username"]
        Password = request.data["Password"]
        email = request.data["Email"]
        try:
            u = User.objects.get(username=Username)
            return JsonResponse(
                "User with this Username Already Exists",
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            u = User.objects.create_user(
                username=Username,
                first_name=First_Name,
                last_name=Last_Name,
                email=email,
            )
            u.save()
            u.set_password(Password)
            u.save()
            token, _ = Token.objects.get_or_create(user=u)
            response = {
                "Name": u.first_name + u.last_name,
                "Email": u.email,
                "Username": u.username,
                "Token": token.key,
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
