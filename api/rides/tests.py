from django.contrib.auth import (
    get_user_model,
)
from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITestCase,
)
from rest_framework.authtoken.models import (
    Token,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)


from ..users.models import (
    Passenger,
    Driver,
)
from ..users.serializers import (
    DriverSerializer,
    PassengerSerializer,
)


User = get_user_model()


class AccountTests(
    APITestCase
):
    @classmethod
    def setUpTestData(cls):
        passenger_data = {
            "user": {
                "username": "mile",
                "password": "test",
                "email": "mile@gmail.com",
            }
        }
        p_serializer = PassengerSerializer(
            data=passenger_data
        )
        if p_serializer.is_valid():
            cls.passenger = p_serializer.save()

        driver_data = {
            "user": {
                "username": "miki",
                "password": "test",
                "email": "miki@gmail.com",
            },
            "car_type": "city",
            "rating": "1.0",
        }
        d_serializer = DriverSerializer(
            data=driver_data
        )
        if d_serializer.is_valid():
            cls.driver = d_serializer.save()

    def test_create_ride_request(
        self,
    ):
        """
        Ensure we can create a ride request
        """
        passenger_user = User.objects.get(
            pk=self.passenger.pk
        )
        token = RefreshToken.for_user(
            user=passenger_user
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(
                token.access_token
            )
        )
        url = reverse(
            "create-ride"
        )
        data = {
            "starting_location": "skopje",
            "destination": "berlin",
        }
        response = (
            self.client.post(
                url,
                data,
                format="json",
            )
        )
        print(response.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
