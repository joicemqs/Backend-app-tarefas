from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # geração da documentação (drf-spectacular) não tem usuário logado
            return Task.objects.none()
        # retorna apenas as tasks do usuário autenticado; tarefas de outros usuários respondem 404
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # atribui o owner automaticamente ao criar
        serializer.save(owner=self.request.user)
