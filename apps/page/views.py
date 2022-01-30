from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.page.models import Tag, Page, Post
from apps.page.serializers import TagSerializer, PageSerializer, PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
