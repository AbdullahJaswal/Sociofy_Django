from rest_framework import serializers
from .models import *


class FacebookAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookAccounts
        fields = [
            'id',
            'facebook_id',
            'length',
            'access_token',
            'reauthorize_in_seconds',
            'signed_request',
            'created_on',
            'expires_on',
            'role',
            'user'
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user  # Sets USER to newly created field.

        return super().create(validated_data)


class InstagramAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccounts
        fields = [
            'id',
            'instagram_id',
            'length',
            'access_token',
            'reauthorize_in_seconds',
            'signed_request',
            'created_on',
            'expires_on',
            'role',
            'user'
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user  # Sets USER to newly created field.

        return super().create(validated_data)
