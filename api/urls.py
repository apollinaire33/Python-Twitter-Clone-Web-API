from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/pages/', include('apps.page.urls')),
    path('api/v1/users/', include('apps.user.urls')),
]
