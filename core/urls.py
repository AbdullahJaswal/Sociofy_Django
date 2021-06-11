"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

import debug_toolbar

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('favicon.ico/', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='users')),
    path('sm_accounts/', include('sm_accounts.urls', namespace='sm_accounts')),
    path('fb_management/', include('fb_management.urls', namespace='fb_management')),
    path('ig_management/', include('ig_management.urls', namespace='ig_management')),
    path('social_analytics/', include('social_analytics.urls', namespace='social_analytics')),
    path('teams/', include('teams.urls', namespace='teams')),
]
