from rest_framework import permissions

from apps.page.models import Page


class PageBasePermission(permissions.BasePermission):
    @staticmethod
    def permission_setup(view):
        page_id = view.kwargs.get('page_pk')
        return Page.objects.get(id=page_id)


class IsPageOwner(PageBasePermission):
    def has_permission(self, request, view):
        page = self.permission_setup(view)
        return request.user == page.owner

    def has_object_permission(self, request, view, obj):
        page = self.permission_setup(view)
        return request.user == page.owner


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.page.owner


class IsPagePrivate(PageBasePermission):
    def has_permission(self, request, view, **kwargs):
        page = self.permission_setup(view)
        return not page.is_private

    def has_object_permission(self, request, view, obj):
        page = self.permission_setup(view)
        return not page.is_private


class IsPageBlocked(PageBasePermission):
    def has_permission(self, request, view):
        page = self.permission_setup(view)
        return not page.is_blocked


class IsPostPageOwner(PageBasePermission):
    def has_permission(self, request, view, **kwargs):
        page = self.permission_setup(view)
        return request.user == page.owner


class IsFollower(PageBasePermission):
    def has_permission(self, request, view):
        page = self.permission_setup(view)
        return request.user in page.followers.all()


class IsSpecifiedPageCorrect(PageBasePermission):
    def has_permission(self, request, view):
        page = self.permission_setup(view)
        return request.data.get('page') == page.id

    def has_object_permission(self, request, view, obj):
        page = self.permission_setup(view)
        return request.data.get('page') == page.id


class IsSpecifiedFollowRequestCorrect(PageBasePermission):
    def has_permission(self, request, view):
        return request.data.get('follow_requests') == [request.user.id]


class IsSpecifiedFollowerCorrect(PageBasePermission):
    def has_permission(self, request, view):
        return request.data.get('followers') == [request.user.id]

    def has_object_permission(self, request, view, obj):
        return request.data.get('followers') == [request.user.id]


class IsSpecifiedLikeCorrect(PageBasePermission):
    def has_permission(self, request, view):
        return request.data.get('likes') == [request.user.id]

    def has_object_permission(self, request, view, obj):
        return request.data.get('likes') == [request.user.id]
