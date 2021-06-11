from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle

from .models import *
from .serializers import *
from .tasks import *

from users.models import User

permission = AllowAny  # Change this to IsAuthenticated

user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# Create your views here.
class IGPageAnalyticList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPageAnalyticSerializer

    def get_queryset(self):
        return IGPageAnalytic.objects.filter(page=self.kwargs.get('pk'))

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=user)

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

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            page = IGPage.objects.select_related('sm_account').get(id=self.kwargs["pk"], user=user)

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
