from rest_framework import generics
from .serializers import *

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

permission = IsAuthenticated


# Create your views here.
class FacebookAccountsList(generics.ListCreateAPIView):  # Change to ONLY CreateAPIView
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FacebookAccountsSerializer

    def get_queryset(self):
        return FacebookAccounts.objects.filter(user=self.request.user.id)

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Create your views here.
class InstagramAccountsList(generics.ListCreateAPIView):  # Change to ONLY CreateAPIView
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    queryset = InstagramAccounts.objects.all()
    serializer_class = InstagramAccountsSerializer

    def get_queryset(self):
        return InstagramAccounts.objects.filter(user=self.request.user.id)

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
