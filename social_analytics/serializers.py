from rest_framework import serializers
from .models import *


class IGPageAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageAnalytic
        fields = '__all__'


class IGPageDemographyAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDemographyAnalytic
        fields = '__all__'
