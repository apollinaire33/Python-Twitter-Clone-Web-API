from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import UserSerializer, UserBlockSerializer, UserLoginSerializer
from apps.user.services import UserAuthentication
from apps.user.permissions import IsUser


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
        'block_user': UserBlockSerializer,
    }

    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'create': (AllowAny,),
        'retrieve': (IsUser,),
        'update': (IsUser,),
        'destroy': (IsUser, IsAdminUser,),
        'block_user': (IsAdminUser,),
    }

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

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
