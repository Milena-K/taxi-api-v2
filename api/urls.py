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
# router.register(r'ride-request', rides_views.RideRequestViewSet, basename="ride-request")
# router.register(r'ride-offer', rides_views.RideOfferViewSet, basename="ride-offer")
# router.register(r'ride-accepted', rides_views.RideAcceptedViewSet, basename="ride-accepted")


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('profile/', views.getProfile),
    path('create-ride/', rides_views.create_ride),
    path('offer-ride/', rides_views.offer_ride),
    path('accept-ride/', rides_views.accept_ride),
    path('start-ride/', rides_views.start_ride_driver),
    # path('request_ride/', rides_views.request_ride),
    # path('rides/', rides_views.list_rides),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
