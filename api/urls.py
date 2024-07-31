from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .users import views
from .rides import views as rides_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'passengers', views.PassengerViewSet, basename="passengers")
router.register(r'drivers', views.DriverViewSet, basename="drivers")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('profile/', views.getProfile),
    path('request_ride/', rides_views.request_ride),
    path('rides/', rides_views.list_rides),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
