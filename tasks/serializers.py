from .models import Task, SubTask
from rest_framework import serializers
from django.utils import timezone


class SubTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'team', 'is_complete', 'completed_date',)

class SubTaskUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = SubTask
        fields = ('id', 'team', 'is_complete', 'completed_date',)

class TaskCreateSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team', 'title', 'content', 'is_complete', 'completed_date','subtasks')

    def create(self, validated_data):

        subtasks_data = validated_data.pop('subtasks')

        task = Task.objects.create(**validated_data)

        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)

        return task

class TaskUpdateSerializer(serializers.ModelSerializer):
    subtasks = SubTaskUpdateSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team', 'title', 'content', 'is_complete', 'completed_date','subtasks')
        read_only_fields = ('id', 'create_user', 'team')

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # sub task 변경
        subtasks_data = validated_data.get('subtasks', None)
        
        if subtasks_data is not None:
            for subtask_data in subtasks_data:
                sub_id = subtask_data.get('id', None)
                
                if sub_id:
                    subtask = SubTask.objects.get(id=sub_id)
                    if not subtask.is_complete:
                        subtask.is_complete = subtask_data.get('is_complete', subtask.is_complete)
                        if subtask.is_complete:
                            subtask.completed_date = timezone.now()
                    subtask.team = subtask_data.get('team', subtask.team)
                    subtask.save()
                else:
                    SubTask.objects.create(task=instance, **subtask_data)

        # update is_complete of task
        all_subtasks = instance.subtasks.all()
        if all_subtasks and all(subtask.is_complete for subtask in all_subtasks):
            instance.is_complete = True
            instance.completed_date = timezone.now()
            instance.save()
        return instance



