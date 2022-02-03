from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_blocked',)

    def update(self, instance, validated_data):
        is_blocked = validated_data.get('is_blocked')
        pages = instance.pages.all()

        if is_blocked:
            for page in pages:
                page.is_blocked = True
                page.save()
        elif not is_blocked:
            for page in instance.pages.all():
                page.is_blocked = False
                page.save()

        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        extra_kwargs = {
            'email': {'validators': []},
            'password': {'validators': []},
        }
