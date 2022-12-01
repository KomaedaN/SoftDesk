from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets

from authentication.models import User
from authentication.serializers import SignupSerializer


class SignupViewset(viewsets.ModelViewSet):
    serializer_class = SignupSerializer

    def get_queryset(self):
        return User.objects.all()
