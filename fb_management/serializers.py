from rest_framework import serializers
from .models import *


class FBPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPage
        fields = '__all__'


class FBPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPost
        fields = '__all__'


class FBScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBScheduledPost
        fields = '__all__'


class FBPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPost
        fields = ['message', 'link', 'media', 'created_time']


class FBPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPostComment
        fields = '__all__'


class FBPostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPostComment
        fields = ['message', 'attachment_type', 'attachment']


class FBPostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPostTag
        fields = '__all__'
