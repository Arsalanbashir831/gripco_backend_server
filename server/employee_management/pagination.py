from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100  

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count, 
            'page': self.page.number, 
            'next': self.page.has_next(),  
            'previous': self.page.has_previous(), 
            'results': data 
        })
