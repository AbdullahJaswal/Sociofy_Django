from rest_framework import pagination
from rest_framework.response import Response

DEFAULT_PAGE_SIZE = 10


class CustomPagination(pagination.PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
