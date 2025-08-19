from rest_framework import serializers
from .models import TasksModel, User

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TasksModel
        fields = ['id', 'title', 'completed', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return TasksModel.objects.create(user=user, **validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)