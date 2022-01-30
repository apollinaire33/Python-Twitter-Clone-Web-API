from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import UserSerializer, UserLoginSerializer
from apps.user.services import UserAuthentication


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=('post',), url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            f'User {serializer.validated_data["email"]} created successfully',
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=('post',), url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = UserAuthentication.generate_access_token(serializer)

        return Response(
            f'Access token: {token}',
            status=status.HTTP_200_OK
        )
