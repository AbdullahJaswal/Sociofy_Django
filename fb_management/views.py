from rest_framework import generics
from .serializers import *

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from core.pagination import CustomPagination

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .tasks import *

from users.models import User

permission = IsAuthenticated  # Change this to IsAuthenticated


# user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# Create your views here.
class FBPageList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageSerializer

    def get_queryset(self):
        return FBPage.objects.filter(user=self.request.user.id)

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        FacebookAccounts.objects.filter(id=1).update(
            access_token="EAAFZAzWeB7YsBAKrEmLdZAjBrotzZA5JZAxF23R6bQQ55ZByh0obnabCLKeKsJGeJ4r8dLnFeirICSwRZCZCfuMmT4BEiNk5wrKnenJJwZCUOsaTz46jYIabsBmb3rXR33SttPRRGvD4aalfMXZAGdbyEZCjQFxtwfBcD7eZA9PXis91ih6WuiXjFk0tfZCvWv02QmEZD")
        InstagramAccounts.objects.filter(id=1).update(
            access_token="EAAFZAzWeB7YsBAKrEmLdZAjBrotzZA5JZAxF23R6bQQ55ZByh0obnabCLKeKsJGeJ4r8dLnFeirICSwRZCZCfuMmT4BEiNk5wrKnenJJwZCUOsaTz46jYIabsBmb3rXR33SttPRRGvD4aalfMXZAGdbyEZCjQFxtwfBcD7eZA9PXis91ih6WuiXjFk0tfZCvWv02QmEZD")

        try:
            userObj = User.objects.get(id=self.request.user.id)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        response = fetch_fb_pages_data(userObj)

        if response:
            return self.list(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_502_BAD_GATEWAY)


class FBPageDetail(generics.RetrieveAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return FBPage.objects.filter(user=self.request.user.id)

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_fb_page_data(kwargs.get('pk'))

            if response:
                return self.retrieve(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostList(generics.ListCreateAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPostSerializer
    lookup_url_kwarg = 'pk'

    # pagination_class = CustomPagination

    def get_queryset(self):
        return FBPost.objects.filter(page=self.kwargs.get('pk'))

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = FBPostCreateSerializer
        return serializer_class

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_fb_posts_data(kwargs.get('pk'), self.request.user.id)  # Local Page ID

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        PAGE = 112531917317825  # kwargs.get('pk') HARD CODED Dummy Page for Create Post!

        page = FBPage.objects.get(page_id=PAGE)

        if page.user_id == self.request.user.id:
            if (request.data['message'] is None and request.data['link'] is None and request.data['media'] is None) or (
                    request.data['message'] == '' and request.data['link'] == '' and request.data['media'] == ''):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_fb_post(page.id, self.request.user.id,
                                          request.data['message'] or None,
                                          request.data['link'] or None,
                                          request.data['media'] or None
                                          )

                if response:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPostSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return FBPost.objects.filter(id=self.kwargs.get('ppk'), page=self.kwargs.get('pk'))

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_fb_post_data(kwargs.get('pk'), self.request.user.id,
                                          kwargs.get('ppk'))  # Local Page ID & Local Post ID

            if response:
                return self.retrieve(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        PAGE = 2  # kwargs.get('pk') HARD CODED Dummy Page for Delete Post!

        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = delete_fb_post(PAGE, self.request.user.id, kwargs.get('ppk'))  # Local Page ID & Local Post ID

            if response:
                return Response(status=status.HTTP_200_OK)
            elif response == 0:
                # If the Post was not posted from the application.
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostCommentList(generics.ListCreateAPIView):
    permission_classes = [permission]
    serializer_class = FBPostCommentSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return FBPostComment.objects.filter(post=self.kwargs.get('ppk'))

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = FBPostCommentCreateSerializer
        return serializer_class

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_fb_post_comments_data(kwargs.get('pk'), kwargs.get('ppk'),
                                                   self.request.user.id)  # Local Page ID & Local Post ID

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        PAGE = 2  # kwargs.get('pk') HARD CODED Dummy Page for Create Post!

        page = FBPage.objects.get(id=PAGE)

        if page.user_id == self.request.user.id:
            if (request.data['message'] is None and request.data['attachment_type'] is None and request.data[
                'attachment'] is None) or (
                    request.data['message'] == '' and request.data['attachment_type'] == '' and request.data[
                'attachment'] == ''):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_fb_post_comment(PAGE, kwargs.get('ppk'), self.request.user.id,
                                                  request.data['message'] or None,
                                                  request.data['attachment_type'] or None,
                                                  request.data['attachment'] or None
                                                  )

                if response:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostCommentDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permission]
    queryset = FBPostComment.objects.all()
    serializer_class = FBPostCommentSerializer
    lookup_url_kwarg = 'cpk'

    def get_queryset(self):
        return FBPostComment.objects.filter(id=self.kwargs.get('cpk'), post=self.kwargs.get('ppk'))

    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_fb_post_comment_data(kwargs.get('pk'), kwargs.get('cpk'),
                                                  self.request.user.id,
                                                  kwargs.get('ppk'))  # Local Page ID & Local Post ID

            if response:
                return self.retrieve(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        PAGE = 2  # kwargs.get('pk') HARD CODED Dummy Page for Delete Post!

        page = FBPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = delete_fb_post_comment(PAGE, self.request.user.id,
                                              kwargs.get('cpk'))  # Local Page ID & Local Comment ID

            if response:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBPostTagsList(generics.ListAPIView):
    permission_classes = [permission]  # Should be IsAdmin
    queryset = FBPostTag.objects.all()
    serializer_class = FBPostTagsSerializer
