import configs
from rest_framework import generics
from .serializers import *

from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator

from django.db.models import Count

from .tasks import *

from users.models import User

from configs import permission, caching


# user = 1  # Replace 'user' to self.request.user.id with FIND and REPLACE and remove this variable.


# Create your views here.
class FBPageList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBPageSerializer

    def get_queryset(self):
        return FBPage.objects.filter(user=self.request.user.id)

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
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

    @method_decorator(caching)
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

    @method_decorator(caching)
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

        page = FBPage.objects.get(page_id=PAGE, user_id=self.request.user.id)

        if page.user_id == self.request.user.id:
            if (request.data['message'] is None and request.data['link'] is None and request.data['media'] is None and
                request.data['created_time'] is None) or (
                    request.data['message'] == '' and request.data['link'] == '' and request.data['media'] == '' and
                    request.data['created_time'] is None):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_fb_post(page.id, self.request.user.id,
                                          message=request.data.get('message') or None,
                                          link=request.data.get('link') or None,
                                          pictures=request.data.get('media') or None,
                                          video=None,
                                          schedule=request.data.get('created_time') or None
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

    @method_decorator(caching)
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
        PAGE = 112531917317825  # kwargs.get('pk') HARD CODED Dummy Page for Delete Post!

        page = FBPage.objects.get(page_id=PAGE, user=self.request.user.id)

        if page.user_id == self.request.user.id:
            response = delete_fb_post(page.id, self.request.user.id, kwargs.get('ppk'))  # Local Page ID & Local Post ID

            if response:
                return Response(status=status.HTTP_200_OK)
            elif response == 0:
                # If the Post was not posted from the application.
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FBScheduledPostList(generics.ListCreateAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    serializer_class = FBScheduledPostSerializer
    lookup_url_kwarg = 'pk'

    # pagination_class = CustomPagination

    def get_queryset(self):
        return FBScheduledPost.objects.filter(page=self.kwargs.get('pk'))

    # @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'), user=self.request.user.id)

        if page.user_id == self.request.user.id:
            response = fetch_fb_scheduled_posts_data(kwargs.get('pk'), self.request.user.id)  # Local Page ID

            if response:
                return self.list(request, *args, **kwargs)
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

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        page = FBPage.objects.get(id=self.kwargs.get('pk'), user=self.request.user.id)

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
        PAGE = 112531917317825  # kwargs.get('pk') HARD CODED Dummy Page for Delete Post!

        page = FBPage.objects.get(page_id=PAGE, user=self.request.user.id)

        if page.user_id == self.request.user.id:
            if (request.data['message'] is None and request.data['attachment_type'] is None and request.data[
                'attachment'] is None) or (
                    request.data['message'] == '' and request.data['attachment_type'] == '' and request.data[
                'attachment'] == ''):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = create_fb_post_comment(page.id, kwargs.get('ppk'), self.request.user.id,
                                                  request.data.get('message') or None,
                                                  request.data.get('attachment_type') or None,
                                                  request.data.get('attachment') or None
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
        page = FBPage.objects.get(id=self.kwargs.get('pk'), user=self.request.user.id)

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
    permission_classes = [configs.AllowAny]  # Should be IsAdmin
    queryset = FBPostTag.objects.all()
    serializer_class = FBPostTagsSerializer

    def get_queryset(self):
        length = 7
        most_occuring = FBPostTag.objects.values_list('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')

        most_occuring_tags = []
        for idx, tag in enumerate(most_occuring):
            if idx < length:
                most_occuring_tags.append(tag[0])
            else:
                break

        tags = FBPostTag.objects.all()
        tag_ids = []
        for idx, tag in enumerate(tags):
            for idx2, m_o_t in enumerate(most_occuring_tags):
                if tag.tag == m_o_t:
                    tag_ids.append(idx)
                    most_occuring_tags.pop(idx2)

            if len(tag_ids) == length:
                break

        return FBPostTag.objects.filter(id__in=tag_ids)

    @method_decorator(caching)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
