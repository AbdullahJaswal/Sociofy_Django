from rest_framework import serializers
from .models import *


class IGPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPage
        fields = '__all__'


class IGPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPost
        fields = '__all__'


class IGPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPost
        fields = ['caption', 'media_type', 'media']


class IGPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPostComment
        fields = '__all__'


class IGPostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPostComment
        fields = ['text']
