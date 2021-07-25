from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .serializers import *
from .tasks import *

from django.utils.decorators import method_decorator

from configs import *


# user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# Create your views here.
class FBPageAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageAnalyticSerializer

    def get_queryset(self):
        return FBPageAnalytic.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_fb_page_analytics_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPageDemographyAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageDemographyAnalyticSerializer

    def get_queryset(self):
        return FBPageDemographyAnalytic.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            if page.likes > 100:
                response = fetch_fb_page_demography_analytics_data(page)
            else:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPageDailyAnalyticsList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageDailyAnalyticsSerializer

    def get_queryset(self):
        return FBPageDailyAnalytics.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_fb_page_daily_analytics_data(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPostAnalyticSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return FBPostAnalytic.objects.filter(post=self.kwargs.get('ppk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_fb_post_analytics_data(page, self.kwargs.get('ppk'))

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostRatingList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPostRatingsSerializer

    def get_queryset(self):
        return FBPostRating.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_fb_post_ratings(page)

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPageAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageAnalyticSerializer

    def get_queryset(self):
        return IGPageAnalytic.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
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

    @method_decorator(caching)
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

    @method_decorator(caching)
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

    @method_decorator(caching)
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


class IGPageDailyAnalyticsNOOUTLIERSList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageDailyAnalyticsNOOUTLIERSSerializer

    def get_queryset(self):
        return IGPageDailyAnalyticsNOOUTLIERS.objects.filter(page=self.kwargs.get('pk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

            response = fetch_ig_page_daily_analytics_data_NO_OUTLIERS(page)

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

    @method_decorator(caching)
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

    @method_decorator(caching)
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

    @method_decorator(caching)
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


class CommentSentimentList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = CommentSentimentSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        if self.kwargs["platform"] == "facebook":
            return CommentSentiment.objects.filter(postFB=self.kwargs.get('ppk'))
        elif self.kwargs["platform"] == "instagram":
            return CommentSentiment.objects.filter(postIG=self.kwargs.get('ppk'))

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        # try:
        page = None
        if self.kwargs["platform"] == "facebook":
            page = FBPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)
        elif self.kwargs["platform"] == "instagram":
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=self.request.user.id)

        response = get_comment_sentiment(page, self.kwargs["platform"], self.kwargs["ppk"])
        return self.list(request, *args, **kwargs)
        # if response:
        #     return self.list(request, *args, **kwargs)
        # else:
        #     return Response(status=status.HTTP_502_BAD_GATEWAY)
    # except:
    #     return Response(status=status.HTTP_403_FORBIDDEN)
