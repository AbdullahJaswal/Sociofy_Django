from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page

limit = 30
permission = IsAuthenticated
permissionAllow = AllowAny
permissionIsAdmin = IsAdminUser
caching = [cache_page(60 * 5), vary_on_cookie]
# caching = []
