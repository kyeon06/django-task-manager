from .models import Task, SubTask
from rest_framework import serializers

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'team', 'is_complete')

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team', 'title', 'content', 'is_complete', 'subtasks')
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)

        return task
