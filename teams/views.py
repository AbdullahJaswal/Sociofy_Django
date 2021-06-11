from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle

from .serializers import *

from fb_management.models import *
from ig_management.models import *
from sm_accounts.models import *

permission = IsAuthenticated  # Change this to IsAuthenticated


# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [permission]
    serializer_class = TeamSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Team.objects.filter(user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        datetime = timezone.now().isoformat()
        print(request.data)
        request.data.update({
            "created_on": datetime,
            "modified_on": datetime,
            "user": self.request.user.id
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        Member.objects.create(
            user=self.request.user,
            team=Team.objects.get(id=serializer.data['id']),
            role=Role.objects.get(id=1),
            added_on=datetime,
            status='joined'
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permission]
    serializer_class = MemberSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Member.objects.filter(team=self.kwargs['_pk'])

    def create(self, request, *args, **kwargs):
        datetime = timezone.now().isoformat()
        request.data.update({
            "added_on": datetime,
            "status": "pending",
            "team": self.kwargs['_pk']
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InviteViewSet(viewsets.ModelViewSet):
    permission_classes = [permission]
    serializer_class = MemberSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Member.objects.filter(user=self.request.user.id, status='pending')

    def update(self, request, *args, **kwargs):
        # try:
        invite = Member.objects.get(id=self.kwargs["pk"], user=self.request.user.id, status='pending')

        if invite:
            datetime = timezone.now().isoformat()
            request.data.update({
                "modified_on": datetime
            })

            team = Team.objects.get(id=invite.team.id)

            if team.fb_page:
                fb_account = FacebookAccounts.objects.get(id=team.fb_page.id)

                FacebookAccounts.objects.create(
                    user=self.request.user,
                    role=invite.role,
                    facebook_id=fb_account.facebook_id,
                    length=fb_account.length,
                    access_token=fb_account.access_token,
                    reauthorize_in_seconds=fb_account.reauthorize_in_seconds,
                    signed_request=fb_account.signed_request,
                    created_on=fb_account.created_on,
                    expires_on=fb_account.expires_on
                )

            if team.ig_page:
                ig_account = InstagramAccounts.objects.get(id=team.ig_page.id)

                InstagramAccounts.objects.create(
                    user=self.request.user,
                    role=invite.role,
                    instagram_id=ig_account.instagram_id,
                    length=ig_account.length,
                    access_token=ig_account.access_token,
                    reauthorize_in_seconds=ig_account.reauthorize_in_seconds,
                    signed_request=ig_account.signed_request,
                    created_on=ig_account.created_on,
                    expires_on=ig_account.expires_on
                )

            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        # except:
        #     return Response(status=status.HTTP_502_BAD_GATEWAY)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permission]
    serializer_class = TaskSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Task.objects.filter(team=self.kwargs['_pk'])

    def create(self, request, *args, **kwargs):
        datetime = timezone.now().isoformat()
        request.data.update({
            "created_on": datetime,
            "team": self.kwargs['_pk']
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
