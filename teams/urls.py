from django.urls import path, include
from rest_framework import routers as routers_default
from rest_framework_nested import routers  # noqa. <-- Used to suppress error highlight.
from .views import *

app_name = 'teams'

# Create a router and register our viewsets with it.
teamRouter = routers.SimpleRouter()
teamRouter.register(r'', TeamViewSet, basename='team')

memberRouter = routers.NestedSimpleRouter(teamRouter, r'', lookup='')
memberRouter.register(r'members', MemberViewSet, basename='member')

taskRouter = routers.NestedSimpleRouter(teamRouter, r'', lookup='')
taskRouter.register(r'tasks', TaskViewSet, basename='task')

inviteRouter = routers.SimpleRouter()
inviteRouter.register(r'invites', InviteViewSet, basename='invite')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(inviteRouter.urls)),
    path('', include(teamRouter.urls)),
    path('', include(memberRouter.urls)),
    path('', include(taskRouter.urls)),
]
