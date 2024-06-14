from rest_framework.pagination import PageNumberPagination

class PagePagination(PageNumberPagination):
    page_query_param = "page_num"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return {
            'num_pages': self.page.paginator.num_pages,
            'page': self.page.number,
            'total_items': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'data': data
        }