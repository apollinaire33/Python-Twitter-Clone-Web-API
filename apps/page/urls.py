from rest_framework import routers

from apps.page.views import TagViewSet, PageViewSet, PostViewSet

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'', PageViewSet)

urlpatterns = [
]

urlpatterns += router.urls
