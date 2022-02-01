from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers import UserSerializer, UserLoginSerializer
from apps.user.services import UserAuthentication


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    default_serializer_class = UserSerializer
    serializer_classes_by_action = {
    }

    default_permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'create': (AllowAny,),
    }

    @action(detail=False, methods=('post',), url_path='login', permission_classes=(AllowAny,))
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = UserAuthentication.generate_access_token(serializer)

        return Response(
            f'Access token: {token}',
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
