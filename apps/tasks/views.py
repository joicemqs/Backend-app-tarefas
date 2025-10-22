from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('-created_at') # Retorna apenas as tarefas do usuário autenticado

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) # Define o proprietário da tarefa como o usuário autenticado