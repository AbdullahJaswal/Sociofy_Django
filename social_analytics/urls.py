from django.urls import path
from .views import *

app_name = 'social_analytics'

urlpatterns = [
    path('instagram/page/<int:pk>/', IGPageAnalyticList.as_view(), name='igPageAnalyticList'),
    path('instagram/page/<int:pk>/demography/', IGPageDemographyAnalyticList.as_view(),
         name='igPageDemographyAnalyticList'),
    path('instagram/page/<int:pk>/impressions/', IGPageDailyImpressionsList.as_view(),
         name='igPageDailyImpressionsList'),
    path('instagram/page/<int:pk>/reach/', IGPageDailyReachList.as_view(),
         name='igPageDailyReachList'),
    path('instagram/page/<int:pk>/follower_count/', IGPageDailyFollowerCountList.as_view(),
         name='igPageDailyFollowerCountList'),
    path('instagram/page/<int:pk>/email_contacts/', IGPageDailyEmailContactsList.as_view(),
         name='igPageDailyEmailContactsList'),
    path('instagram/page/<int:pk>/phone_call_clicks/', IGPageDailyPhoneCallClicksList.as_view(),
         name='igPageDailyPhoneCallClicksList'),
    path('instagram/page/<int:pk>/text_message_clicks/', IGPageDailyTextMessageClicksList.as_view(),
         name='igPageDailyTextMessageClicksList'),
    path('instagram/page/<int:pk>/directions_clicks/', IGPageDailyDirectionsClicksList.as_view(),
         name='igPageDailyDirectionsClicksList'),
    path('instagram/page/<int:pk>/website_clicks/', IGPageDailyWebsiteClicksList.as_view(),
         name='igPageDailyWebsiteClicksList'),
    path('instagram/page/<int:pk>/profile_views/', IGPageDailyProfileViewsList.as_view(),
         name='igPageDailyProfileViewsList'),
    path('instagram/page/<int:pk>/post/<int:ppk>/', IGPostAnalyticList.as_view(), name='igPostAnalyticList'),
    path('instagram/page/<int:pk>/ratings/', IGPostRatingList.as_view(), name='igPostRatingList'),
]
