from django.urls import path
from .views import *

app_name = 'ig_management'

urlpatterns = [
    path('pages/', IGPageList.as_view(), name='igPageList'),
    path('pages/<int:pk>/', IGPageDetail.as_view(), name='igPageList'),
    path('pages/<int:pk>/posts/', IGPostList.as_view(), name='igPostList'),
    path('pages/<int:pk>/posts/<int:ppk>/', IGPostDetail.as_view(), name='igPostDetail'),
    path('pages/<int:pk>/posts/<int:ppk>/comments/', IGPostCommentList.as_view(), name='igPostCommentsList'),
    path('pages/<int:pk>/posts/<int:ppk>/comments/<int:cpk>/', IGPostCommentDetail.as_view(),
         name='igPostCommentsDetail'),
]
