from django.urls import path, include
from rest_framework import routers

from apps.user.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
