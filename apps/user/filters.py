from rest_framework import filters


class UserSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if 'username' in request.query_params:
            return ['username']
