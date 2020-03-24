from rest_framework.pagination import PageNumberPagination

class AuthorPagination(PageNumberPagination):
    page_size = 6
