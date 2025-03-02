from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .rides import views as rides_views
from .users import views

router = routers.DefaultRouter()
router.register(
    r"users",
    views.UserViewSet,
    basename="users",
)
router.register(
    r"passengers",
    views.PassengerViewSet,
    basename="passengers",
)
router.register(
    r"drivers",
    views.DriverViewSet,
    basename="drivers",
)
# router.register(
#     "profile",
#     views.ProfileViewSet,
#     basename="profile",
# )
router.register(
    r"rides",
    rides_views.RidesViewSet,
    basename="rides",
)
router.register(
    r"ride-ratings",
    rides_views.RideRatingsViewSet,
    basename="ride-ratings",
)

urlpatterns = [
    # re_path('^rides/(?P<ride_uuid>.+)/$',
    # rides_views.RidesViewSet.as_view({'get':'list'})),
    path(
        "",
        include(router.urls),
    ),
    path(
        "profile/<int:pk>/",
        views.ProfileViewSet.as_view({"patch": "update"}),
    ),
    path(
        "profile/<int:pk>/",
        views.ProfileViewSet.as_view({"get": "retrieve"}),
    ),
    path(
        "register/",
        views.UserViewSet.as_view({"post": "create"}),
    ),
    path(
        "login/",
        views.LoginView.as_view(),
    ),
    path(
        "rate-ride/",
        rides_views.rate_ride,
        name="rate-ride",
    ),
    path(
        "request-ride/",
        rides_views.request_ride,
        name="request-ride",
    ),
    path(
        "offer-ride/",
        rides_views.offer_ride,
    ),
    path(
        "accept-ride/",
        rides_views.accept_ride,
    ),
    path(
        "start-ride/",
        rides_views.start_ride,
    ),
    path(
        "finish-ride/",
        rides_views.finish_ride,
    ),
    path(
        "cancel-ride/",
        rides_views.cancel_ride,
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework",
        ),
    ),
]
