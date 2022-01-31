from rest_framework import serializers

from apps.page.models import Tag, Post, Page


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            'tags',
            'owner',
            'followers',
            'image',
            'is_private',
            'follow_requests',
            'unblock_date',
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'created_at', 'updated_at',)
