"""
A simple page number based style that supports page numbers as
query parameters. For example:

http://api.example.org/accounts/?page=4
http://api.example.org/accounts/?page=4&page_size=100
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
