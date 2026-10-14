from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'is_completed', 'position', 'created_at', 'updated_at', 'due_date']
        # a posição só muda pelo endpoint /reorder/
        read_only_fields = ['id', 'owner', 'position', 'created_at', 'updated_at']


class TaskReorderSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="IDs das tarefas na nova ordem (pode ser só uma parte delas, ex.: as que aparecem num filtro).",
    )

    def validate_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("A lista contém IDs repetidos.")

        user = self.context['request'].user
        found = Task.objects.filter(owner=user, id__in=value).count()
        if found != len(value):
            raise serializers.ValidationError("Uma ou mais tarefas não foram encontradas.")
        return value
