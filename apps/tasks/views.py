from django.db import transaction
from django.db.models import Min
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskReorderSerializer

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
        # atribui o owner automaticamente e coloca a tarefa nova no topo da lista
        lowest = self.get_queryset().aggregate(Min('position'))['position__min']
        position = lowest - 1 if lowest is not None else 0
        serializer.save(owner=self.request.user, position=position)

    @extend_schema(
        summary="Reordenar tarefas",
        description=(
            "Recebe os IDs das tarefas na nova ordem. Pode ser só uma parte das tarefas "
            "(por exemplo, as que aparecem num filtro): elas trocam de lugar entre si e as demais não mudam."
        ),
        request=TaskReorderSerializer,
        responses={200: TaskSerializer(many=True)},
    )
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        serializer = TaskReorderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        with transaction.atomic():
            tasks = {task.id: task for task in self.get_queryset().select_for_update().filter(id__in=ids)}
            # reaproveita as posições que essas tarefas já ocupavam, só que na nova ordem
            positions = sorted(task.position for task in tasks.values())
            reordered = [tasks[task_id] for task_id in ids]
            for task, position in zip(reordered, positions):
                task.position = position
            Task.objects.bulk_update(reordered, ['position'])

        return Response(TaskSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
