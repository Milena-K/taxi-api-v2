from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from .users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# TODO: check which endpoint gets hit...
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
