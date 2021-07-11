from rest_framework import generics
from .serializers import *

from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .tasks import *

from users.models import User

from configs import permission


# user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# # Create your views here.
class IGPageList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    queryset = IGPage.objects.all()
    serializer_class = IGPageSerializer

    def get_queryset(self):
        return IGPage.objects.filter(user=self.request.user.id)

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        try:
            userObj = User.objects.get(id=self.request.user.id)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        response = fetch_ig_pages_data(userObj)

        if response:
            return self.list(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_502_BAD_GATEWAY)


class IGPageDetail(generics.RetrieveAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    queryset = IGPage.objects.all()
    serializer_class = IGPageSerializer
    lookup_url_kwarg = 'pk'

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_ig_page_data(kwargs.get('pk'))

            if response:
                return self.retrieve(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostList(generics.ListCreateAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPostSerializer
    lookup_url_kwarg = 'pk'

    # pagination_class = CustomPagination

    def get_queryset(self):
        return IGPost.objects.filter(page=self.kwargs.get('pk'))

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = IGPostCreateSerializer
        return serializer_class

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_ig_posts_data(kwargs.get('pk'), self.request.user.id)  # Local Page ID

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        PAGE = 17841446538771918  # kwargs.get('pk') HARD CODED Dummy Page for Create Post!

        page = IGPage.objects.get(page_id=PAGE, user_id=self.request.user.id)

        if page.user_id == self.request.user.id:
            if (request.data['caption'] is None and request.data['media_type'] is None and request.data[
                'media'] is None) or (
                    request.data['caption'] == '' and request.data['media_type'] == '' and request.data['media'] == ''):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_ig_post(page.id, self.request.user.id,
                                          request.data['caption'] or None,
                                          request.data['media_type'] or None,
                                          request.data['media'] or None
                                          )

                if response:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = IGPostSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return IGPost.objects.filter(id=self.kwargs.get('ppk'), page=self.kwargs.get('pk'))

    # @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_ig_post_data(kwargs.get('pk'), self.request.user.id,
                                          kwargs.get('ppk'))  # Local Page ID & Local Post ID

            if response:
                return self.retrieve(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostCommentList(generics.ListCreateAPIView):
    permission_classes = [permission]
    serializer_class = IGPostCommentSerializer
    lookup_url_kwarg = 'ppk'

    def get_queryset(self):
        return IGPostComment.objects.filter(post=self.kwargs.get('ppk'))

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = IGPostCommentCreateSerializer
        return serializer_class

    @method_decorator(cache_page(60 * 5))  # Cached for 5 minutes.
    def get(self, request, *args, **kwargs):
        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_ig_post_comments_data(kwargs.get('pk'), kwargs.get('ppk'),
                                                   self.request.user.id)  # Local Page ID & Local Post ID

            if response:
                return self.list(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        PAGE = 2  # kwargs.get('pk') HARD CODED Dummy Page for Create Post!

        page = IGPage.objects.get(id=PAGE)

        if page.user_id == self.request.user.id:
            if request.data['text'] is None or request.data['text'] == '':
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_ig_post_comment(PAGE, kwargs.get('ppk'), self.request.user.id,
                                                  request.data['text'] or None
                                                  )

                if response:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IGPostCommentDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permission]
    queryset = IGPostComment.objects.all()
    serializer_class = IGPostCommentSerializer
    lookup_url_kwarg = 'cpk'

    def get_queryset(self):
        return IGPostComment.objects.filter(id=self.kwargs.get('cpk'), post=self.kwargs.get('ppk'))

    def get(self, request, *args, **kwargs):
        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = fetch_ig_post_comment_data(kwargs.get('pk'), kwargs.get('cpk'),
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

        page = IGPage.objects.get(id=self.kwargs.get('pk'))

        if page.user_id == self.request.user.id:
            response = delete_ig_post_comment(PAGE, self.request.user.id,
                                              kwargs.get('cpk'))  # Local Page ID & Local Comment ID

            if response:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
