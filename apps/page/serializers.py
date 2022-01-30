from rest_framework import serializers

from apps.page.models import Tag, Post, Page


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
