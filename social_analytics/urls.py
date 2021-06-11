from django.urls import path
from .views import *

app_name = 'social_analytics'

urlpatterns = [
    path('instagram/<int:pk>/page/', IGPageAnalyticList.as_view(), name='igPageAnalyticList'),
    path('instagram/<int:pk>/page/demography/', IGPageDemographyAnalyticList.as_view(),
         name='igPageDemographyAnalyticList'),
]
