from rest_framework.pagination import LimitOffsetPagination


class CustomizedPostPagination(LimitOffsetPagination):
    max_limit = 250
    default_limit = 25
