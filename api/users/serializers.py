from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    serializers,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from django.contrib.auth.hashers import (
    make_password,
)
from .models import (
    Passenger,
    Driver,
)


User = get_user_model()


class UserSerializer(
    serializers.HyperlinkedModelSerializer
):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "profile_picture",
            "password",
            "pk",
        ]
        # extra_kwargs = {'id': {'read_only': True, 'required': True}}

    def validate_password(
        self, password: str
    ):
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(
            password
        )


class MyTokenObtainPairSerializer(
    TokenObtainPairSerializer
):
    @classmethod
    def get_token(cls, user):
        token = (
            super().get_token(
                user
            )
        )
        token["username"] = (
            user.username
        )

        return token


class PassengerSerializer(
    serializers.HyperlinkedModelSerializer
):
    user = UserSerializer()
    user_pk = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Passenger
        fields = [
            "user",
            "rides_taken",
            "user_pk",
        ]
        depth = 1

    def create(
        self, validated_data
    ):
        user_data = validated_data.pop(
            "user"
        )
        user = User.objects.create(
            **user_data
        )
        passenger = Passenger.objects.create(
            user=user,
            **validated_data,
        )
        return passenger

    def update(
        self,
        instance,
        validated_data,
    ):
        instance.credit_card = validated_data.get(
            "credit_card"
        )
        instance.save()

        nested_serializer = (
            self.fields[
                "user"
            ]
        )
        nested_instance = (
            instance.user
        )
        nested_data = validated_data.pop(
            "user"
        )
        nested_serializer.update(
            nested_instance,
            nested_data,
        )
        return instance


class DriverSerializer(
    serializers.HyperlinkedModelSerializer
):
    user = UserSerializer()
    user_pk = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Driver
        fields = [
            "user",
            "car_type",
            "rating",
            "user_pk",
        ]
        depth = 1

    def create(
        self, validated_data
    ):
        user_data = validated_data.pop(
            "user"
        )
        user = User.objects.create(
            **user_data
        )
        driver = Driver.objects.create(
            user=user,
            **validated_data,
        )
        return driver

    def update(
        self,
        instance,
        validated_data,
    ):
        instance.car_type = validated_data.get(
            "car_type"
        )
        instance.rating = validated_data.get(
            "rating"
        )
        instance.save()

        nested_serializer = (
            self.fields[
                "user"
            ]
        )
        nested_instance = (
            instance.user
        )
        nested_data = validated_data.pop(
            "user"
        )
        nested_serializer.update(
            nested_instance,
            nested_data,
        )
        return instance


class UserProfileSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "phone_number",
            "profile_picture",
            "birthday",
        ]
