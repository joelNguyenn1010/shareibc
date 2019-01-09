from rest_framework import pagination, response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 30
    # max_limit = 1

    def get_paginated_response(self, data):
        return response.Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'items_per_page': self.page_size,
            'results': data,

        })