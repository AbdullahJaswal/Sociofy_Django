from rest_framework import serializers
from .models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    member = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'
