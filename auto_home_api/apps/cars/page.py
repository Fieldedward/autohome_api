from rest_framework.pagination import PageNumberPagination


class CommonPageNumberPagination(PageNumberPagination):
    page_size = 8

    page_query_param = 'page'

    page_size_query_param = 'page_size'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 10
