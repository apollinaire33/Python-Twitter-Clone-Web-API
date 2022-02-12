from django.conf import settings
from rest_framework import serializers

from apps.user.models import User
from apps.user.services import Avatar


class UserAppSerializer(serializers.ModelSerializer):
    @staticmethod
    def get_field_value(validated_data, field_name, is_list=False):
        try:
            field_value = validated_data.get(field_name)[0] if is_list else validated_data.get(field_name)
        except IndexError:
            field_value = []

        return field_value


class UserSerializer(UserAppSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserDetailSerializer(UserAppSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar',)

    def to_representation(self, obj):
        request = self.context.get("request")
        user = super().to_representation(obj)
        return Avatar.set_serializer_avatar(request, serializable_instance=user, obj=obj)


class UserBlockSerializer(UserAppSerializer):
    class Meta:
        model = User
        fields = ('is_blocked',)

    def update(self, instance, validated_data):
        is_blocked = validated_data.get('is_blocked')
        pages = instance.pages.all()

        if is_blocked:
            pages.update(is_blocked=True)
        elif not is_blocked:
            pages.update(is_blocked=False)

        return super().update(instance, validated_data)


class UserLoginSerializer(UserAppSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        extra_kwargs = {
            'email': {'validators': []},
            'password': {'validators': []},
        }


class UserURLSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        image = self.get_field_value(validated_data=validated_data, field_name='avatar')

        return Avatar().set_instance_avatar(
            request, image, instance,
            avatar_folder=settings.AWS_S3_USER_PROFILE_FOLDER,
            base_photo=settings.AWS_S3_BASE_USER_PROFILE_PHOTO,
        )
