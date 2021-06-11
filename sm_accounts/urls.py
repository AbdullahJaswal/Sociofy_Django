from django.urls import path
from .views import *

app_name = 'sm_accounts'

urlpatterns = [
    path('facebook/accounts/', FacebookAccountsList.as_view(), name='facebookAccountsList'),
    path('instagram/accounts/', InstagramAccountsList.as_view(), name='facebookAccountsList')
]
