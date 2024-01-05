from rest_framework.pagination import LimitOffsetPagination


class MessagePagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 250
