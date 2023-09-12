from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """Pagination for is designed for 20 elements per page"""

    page_size = 20
    page_query_param = "currentPage"

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )
