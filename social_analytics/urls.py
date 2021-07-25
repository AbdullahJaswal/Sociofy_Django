from django.urls import path
from .views import *

app_name = 'social_analytics'

urlpatterns = [
    path('facebook/page/<int:pk>/', FBPageAnalyticList.as_view(), name='fbPageAnalyticList'),
    path('facebook/page/<int:pk>/demography/', FBPageDemographyAnalyticList.as_view(),
         name='fbPageDemographyAnalyticList'),
    path('facebook/page/<int:pk>/analytics/', FBPageDailyAnalyticsList.as_view(),
         name='fbPageDailyAnalyticsList'),
    path('facebook/page/<int:pk>/post/<int:ppk>/', FBPostAnalyticList.as_view(), name='fbPostAnalyticList'),
    path('facebook/page/<int:pk>/ratings/', FBPostRatingList.as_view(), name='fbPostRatingList'),

    path('instagram/page/<int:pk>/', IGPageAnalyticList.as_view(), name='igPageAnalyticList'),
    path('instagram/page/<int:pk>/demography/', IGPageDemographyAnalyticList.as_view(),
         name='igPageDemographyAnalyticList'),
    path('instagram/page/<int:pk>/correlation/', IGPageMetricsCorrelationList.as_view(),
         name='igPageMetricsCorrelationList'),
    path('instagram/page/<int:pk>/analytics/', IGPageDailyAnalyticsList.as_view(),
         name='igPageDailyAnalyticsList'),
    path('instagram/page/<int:pk>/analytics_no_outliers/', IGPageDailyAnalyticsNOOUTLIERSList.as_view(),
         name='igPageDailyAnalyticsNOOUTLIERSList'),
    path('instagram/page/<int:pk>/post/<int:ppk>/', IGPostAnalyticList.as_view(), name='igPostAnalyticList'),
    path('instagram/page/<int:pk>/ratings/', IGPostRatingList.as_view(), name='igPostRatingList'),
    path('instagram/page/<int:pk>/best_time/', IGBestPostTimeList.as_view(), name='igBestPostTimeList'),
    path('<str:platform>/<int:pk>/posts/<int:ppk>/comments/', CommentSentimentList.as_view(),
         name='CommentSentimentList'),
]
