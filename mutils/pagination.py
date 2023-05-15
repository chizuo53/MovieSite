from rest_framework.pagination import PageNumberPagination

class GenericPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'p'
    last_page_strings = ('last', 'l')


class MoviePageNumberPagination(GenericPageNumberPagination):
    pass

class SpiderPageNumberPagination(GenericPageNumberPagination):
    pass

class UserPageNumberPagination(GenericPageNumberPagination):
    pass

class UserLikePageNumberPagination(GenericPageNumberPagination):
    pass

