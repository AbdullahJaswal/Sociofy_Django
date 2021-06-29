from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .serializers import *
from .tasks import *

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from configs import *


# user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# Create your views here.
class IGPageAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageAnalyticSerializer

    def get_queryset(self):
        return IGPageAnalytic.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_analytics_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDemographyAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDemographyAnalyticSerializer

    def get_queryset(self):
        return IGPageDemographyAnalytic.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            if page.followers_count > 100:
                response = fetch_ig_page_demography_analytics_data(page)
            else:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageMetricsCorrelationList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageMetricsCorrelationSerializer

    def get_queryset(self):
        return IGPageMetricsCorrelation.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_metrics_correlation_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyAnalyticsList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyAnalyticsSerializer

    def get_queryset(self):
        return IGPageDailyAnalytics.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_analytics_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyImpressionsList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyImpressionsSerializer

    def get_queryset(self):
        return IGPageDailyImpressions.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_impressions_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyReachList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyReachSerializer

    def get_queryset(self):
        return IGPageDailyReach.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_reach_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyFollowerCountList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyFollowerCountSerializer

    def get_queryset(self):
        return IGPageDailyFollowerCount.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_follower_count_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyEmailContactsList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyEmailContactsSerializer

    def get_queryset(self):
        return IGPageDailyEmailContacts.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_email_contacts_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyPhoneCallClicksList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyPhoneCallClicksSerializer

    def get_queryset(self):
        return IGPageDailyPhoneCallClicks.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_phone_call_clicks_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyTextMessageClicksList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyTextMessageClicksSerializer

    def get_queryset(self):
        return IGPageDailyTextMessageClicks.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_text_message_clicks_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyDirectionsClicksList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyDirectionsClicksSerializer

    def get_queryset(self):
        return IGPageDailyDirectionsClicks.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_directions_clicks_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyWebsiteClicksList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyWebsiteClicksSerializer

    def get_queryset(self):
        return IGPageDailyWebsiteClicks.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_website_clicks_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageDailyProfileViewsList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyProfileViewsSerializer

    def get_queryset(self):
        return IGPageDailyProfileViews.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_profile_views_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPostAnalyticSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return IGPostAnalytic.objects.filter(post=self.kwargs.get('ppk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_post_analytics_data(page, self.kwargs.get('ppk'))

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostRatingList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPostRatingsSerializer

    def get_queryset(self):
        return IGPostRating.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_post_ratings(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGBestPostTimeList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGBestPostTimeSerializer

    def get_queryset(self):
        return IGBestPostTime.objects.filter(page=self.kwargs.get('pk'))

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = calculate_best_post_time(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
