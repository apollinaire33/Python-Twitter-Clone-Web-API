from rest_framework import routers

from apps.user.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
]

urlpatterns += router.urls
