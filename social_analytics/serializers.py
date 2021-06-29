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


class IGPageMetricsCorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageMetricsCorrelation
        fields = '__all__'


class IGPageDailyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyAnalytics
        fields = '__all__'


class IGPageDailyImpressionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyImpressions
        fields = '__all__'


class IGPageDailyReachSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyReach
        fields = '__all__'


class IGPageDailyFollowerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyFollowerCount
        fields = '__all__'


class IGPageDailyEmailContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyEmailContacts
        fields = '__all__'


class IGPageDailyPhoneCallClicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyPhoneCallClicks
        fields = '__all__'


class IGPageDailyTextMessageClicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyTextMessageClicks
        fields = '__all__'


class IGPageDailyDirectionsClicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyDirectionsClicks
        fields = '__all__'


class IGPageDailyWebsiteClicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyWebsiteClicks
        fields = '__all__'


class IGPageDailyProfileViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPageDailyProfileViews
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
