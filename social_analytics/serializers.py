from rest_framework import serializers
from .models import *


class FBPageAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPageAnalytic
        fields = '__all__'


class FBPageDemographyAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPageDemographyAnalytic
        fields = '__all__'


class FBPageDailyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPageDailyAnalytics
        fields = '__all__'


class FBPostAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPostAnalytic
        fields = '__all__'


class FBPostRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBPostRating
        fields = '__all__'


class IGPageAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageAnalytic
        fields = '__all__'


class IGPageDemographyAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDemographyAnalytic
        fields = '__all__'


class IGPageMetricsCorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageMetricsCorrelation
        fields = '__all__'


class IGPageDailyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyAnalytics
        fields = '__all__'


class IGPageDailyAnalyticsNOOUTLIERSSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyAnalyticsNOOUTLIERS
        fields = '__all__'


class IGPostAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPostAnalytic
        fields = '__all__'


class IGPostRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPostRating
        fields = '__all__'


class IGBestPostTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGBestPostTime
        fields = '__all__'


class CommentSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSentiment
        fields = '__all__'
