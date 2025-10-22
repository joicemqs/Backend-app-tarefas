from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

