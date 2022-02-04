from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from apps.page.models import Tag, Page, Post
from apps.page.serializers import (
    TagSerializer,
    PageSerializer,
    PageBlockSerializer,
    PageDetailSerializer,
    PageFollowRequestSerializer,
    PageFollowersSerializer,
    PageLikedPostsSerializer,
    PostSerializer,
    PostLikesSerializer,
)
from apps.page.permissions import (
    IsPageOwner,
    IsPostOwner,
    IsPagePrivate,
    IsPageBlocked,
    IsPostPageOwner,
    IsFollower,
    IsSpecifiedPageCorrect,
    IsSpecifiedFollowRequestCorrect,
    IsSpecifiedFollowerCorrect,
    IsSpecifiedLikeCorrect,
)
from apps.user.permissions import IsModeratorUser


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class PageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Page.objects.all()

    serializer_class = PageSerializer
    serializer_classes_by_action = {
        'create': PageDetailSerializer,
        'retrieve': PageDetailSerializer,
        'update': PageDetailSerializer,
        'follow_requests': PageFollowRequestSerializer,
        'add_follow_request': PageFollowRequestSerializer,
        'remove_follow_request': PageFollowRequestSerializer,
        'followers': PageFollowersSerializer,
        'add_follower': PageFollowersSerializer,
        'remove_follower': PageFollowersSerializer,
        'liked_posts': PageLikedPostsSerializer,
        'block_page': PageBlockSerializer,
    }

    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'retrieve': (IsPageBlocked | IsModeratorUser | IsAdminUser),
        'update': (IsPageOwner, IsPageBlocked),
        'destroy': (IsPageOwner,),
        'add_follow_request': (IsSpecifiedFollowRequestCorrect,),
        'remove_follow_request': (IsSpecifiedFollowRequestCorrect | IsPageOwner,),
        'add_follower': (
            (~IsPageOwner & IsSpecifiedFollowerCorrect & IsPagePrivate) | (~IsPagePrivate & IsPageOwner),
        ),
        'remove_follower': (IsSpecifiedFollowerCorrect | IsPageOwner,),
        'liked_posts': (IsPageOwner, IsPageBlocked,),
        'block_page': (IsModeratorUser | IsAdminUser,)
    }

    lookup_url_kwarg = 'page_pk'

    @action(detail=True, methods=('GET',), url_path='follow-requests')
    def follow_requests(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @follow_requests.mapping.post
    def add_follow_request(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @follow_requests.mapping.delete
    def remove_follow_request(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=('GET',), url_path='followers')
    def followers(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @followers.mapping.post
    def add_follower(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @followers.mapping.delete
    def remove_follower(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=('GET',), url_path='liked_posts')
    def liked_posts(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=('PATCH',))
    def block_page(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    serializer_classes_by_action = {
        'like_post': PostLikesSerializer,
        'unlike_post': PostLikesSerializer,
    }

    permission_classes = (IsAuthenticated | IsAdminUser,)
    permission_classes_by_action = {
        'list': (
            IsPagePrivate | IsPostPageOwner | IsFollower | IsModeratorUser | IsAdminUser,
            IsPageBlocked | IsModeratorUser | IsAdminUser,
        ),
        'create': (IsPostPageOwner, IsSpecifiedPageCorrect,),
        'update': (IsPostOwner,),
        'delete': (IsPostOwner | IsModeratorUser | IsAdminUser,),
        'like_post': (IsSpecifiedLikeCorrect,),
        'unlike_post': (IsSpecifiedLikeCorrect,),
    }

    def list(self, request, pk=None, page_pk=None):
        queryset = Post.objects.filter(page=page_pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=('POST',), url_path='likes')
    def like_post(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @like_post.mapping.delete
    def unlike_post(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
