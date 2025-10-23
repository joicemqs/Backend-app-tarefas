from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # retorna apenas as tasks do usuário autenticado
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # atribui o owner automaticamente ao criar
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # leitura/escrita só para autenticados; object-level verificação pode ser feita no override de get_object
        return [permission() for permission in self.permission_classes]

