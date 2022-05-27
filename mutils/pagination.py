from rest_framework.pagination import PageNumberPagination

class MoviePageNumberPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'p'
    last_page_strings = ('last', 'l')
