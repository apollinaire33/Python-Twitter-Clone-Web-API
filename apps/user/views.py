from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserBlockSerializer,
    UserLoginSerializer,
    UserURLSerializer,
)
from apps.user.services import UserAuthentication
from apps.user.permissions import IsUser
from apps.user.filters import UserSearchFilter


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    serializer_classes_by_action = {
        'retrieve': UserDetailSerializer,
        'block_user': UserBlockSerializer,
        'user_image': UserURLSerializer,
        'update_image': UserURLSerializer,
        'delete_image': UserURLSerializer,
    }

    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'create': (AllowAny,),
        'retrieve': (IsUser | IsAdminUser,),
        'update': (IsUser,),
        'destroy': (IsUser, IsAdminUser,),
        'block_user': (IsAdminUser,),
        'page_image': (IsUser | IsAdminUser,),
        'update_image': (IsUser,),
        'delete_image': (IsUser,),
    }

    filter_backends = (UserSearchFilter,)

    @action(detail=False, methods=('POST',), url_path='login', permission_classes=(AllowAny,))
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = UserAuthentication.generate_access_token(serializer)

        return Response(
            f'Access token: {token}',
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=('PUT',))
    def block_user(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=('GET',))
    def user_image(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @user_image.mapping.put
    def update_image(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @user_image.mapping.delete
    def delete_image(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
