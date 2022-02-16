from rest_framework import filters


class PageSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if 'uuid' in request.query_params:
            return ['uuid']
        if 'name' in request.query_params:
            return ['name']
        if 'tags' in request.query_params:
            return ['tags__name']
