from django.urls import path
from .views import *

app_name = 'fb_management'

urlpatterns = [
    path('pages/', FBPageList.as_view(), name='fbPageList'),
    path('pages/<int:pk>/', FBPageDetail.as_view(), name='fbPageList'),
    path('pages/<int:pk>/posts/', FBPostList.as_view(), name='fbPostList'),
    path('pages/<int:pk>/scheduled_posts/', FBScheduledPostList.as_view(), name='fbScheduledPostList'),
    path('pages/<int:pk>/posts/<int:ppk>/', FBPostDetail.as_view(), name='fbPostDetail'),
    path('pages/<int:pk>/posts/<int:ppk>/comments/', FBPostCommentList.as_view(), name='fbPostCommentsList'),
    path('pages/<int:pk>/posts/<int:ppk>/comments/<int:cpk>/', FBPostCommentDetail.as_view(),
         name='fbPostCommentsDetail'),
    path('tags/', FBPostTagsList.as_view(), name='fbPostTagsList'),
]
