from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.page.tasks import new_post_notification
from apps.page.models import Tag, Post, Page
from apps.user.serializers import UserSerializer
from apps.user.services import Avatar


class PageAppSerializer(serializers.ModelSerializer):
    @staticmethod
    def get_field_value(validated_data, field_name, is_list=False):
        try:
            field_value = validated_data.get(field_name)[0] if is_list else validated_data.get(field_name)
        except IndexError:
            field_value = []

        return field_value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(PageAppSerializer):
    class Meta:
        model = Post
        fields = ('page', 'content', 'reply_to', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'GET':
            fields['reply_to'] = PostSerializer(read_only=True)

        return fields

    def create(self, validated_data):
        page = validated_data.get('page')
        post_content = validated_data.get('content')
        followers = page.followers.all()

        for follower in followers:
            new_post_notification.delay(recipient=follower.email, page_name=page.name, content=post_content)

        return super().create(validated_data)


class PostLikesSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'page', 'likes',)
        read_only_fields = ('id', 'content', 'page',)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        likes = self.get_field_value(validated_data, field_name='likes', is_list=True)

        if likes:
            if request.method == 'PUT':
                instance.likes.add(likes)
            elif request.method == 'DELETE':
                instance.likes.remove(likes)

        instance.save()
        return instance


class PageSerializer(PageAppSerializer):
    owner = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=False)

    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'tags',
            'owner',
            'avatar',
            'is_private',
        )


class PageBlockSerializer(PageAppSerializer):
    class Meta:
        model = Page
        fields = (
            'is_blocked',
            'unblock_date',
        )


class PageDetailSerializer(PageSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            'tags',
            'owner',
            'avatar',
            'is_private',
        )

    def to_representation(self, obj):
        request = self.context.get("request")
        page = super().to_representation(obj)
        return Avatar.set_serializer_avatar(request, serializable_instance=page, obj=obj)


class PageFollowRequestSerializer(PageSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests',)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        follow_request = self.get_field_value(validated_data, field_name='follow_requests', is_list=True)

        if follow_request:
            if request.method == 'PUT':
                instance.follow_requests.add(follow_request)
            elif request.method == 'DELETE':
                instance.follow_requests.remove(follow_request)
        elif request.method == 'DELETE' and len(follow_request) == 0:
            if instance.owner != request.user:
                raise PermissionDenied

            instance.follow_requests.set([])

        instance.save()
        return instance

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'GET':
            fields['follow_requests'] = UserSerializer(many=True, read_only=True)

        return fields


class PageFollowersSerializer(PageSerializer):
    class Meta:
        model = Page
        fields = ('followers',)

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context.get("request")
        followers = self.get_field_value(validated_data, field_name='followers', is_list=True)

        if followers:
            if request.method == 'PUT':
                instance.follow_requests.remove(followers)
                instance.followers.add(followers)
            elif request.method == 'DELETE':
                instance.followers.remove(followers)
        elif request.method == 'PUT' and len(followers) == 0:
            if instance.owner != request.user:
                raise PermissionDenied

            follow_request_list = instance.follow_requests.all()
            for follow_request in follow_request_list:
                instance.follow_requests.remove(follow_request)
                instance.followers.add(follow_request)

        instance.save()
        return instance

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'GET':
            fields['followers'] = UserSerializer(many=True, read_only=True)

        return fields


class PageLikedPostsSerializer(PageSerializer):
    liked_posts = PostLikesSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ('liked_posts',)


class PageURLSerializer(PageDetailSerializer):
    class Meta:
        model = Page
        fields = ('avatar',)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        image = self.get_field_value(validated_data=validated_data, field_name='avatar')

        return Avatar().set_instance_avatar(
            request, image, instance,
            avatar_folder=settings.AWS_S3_PAGE_PROFILE_FOLDER,
            base_photo=settings.AWS_S3_BASE_PAGE_PROFILE_PHOTO,
        )
