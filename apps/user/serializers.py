from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'email': {'validators': []},
            'password': {'validators': []},
        }
