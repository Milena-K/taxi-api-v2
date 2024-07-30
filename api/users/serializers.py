from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from .models import Passenger


User = get_user_model()



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'password']
        extra_kwargs = {'id': {'read_only': True, 'required': True}}

    def validate_password(self, password: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(password)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Passenger
        fields = ['credit_card', 'user']
        depth = 1

    # tested, works nicely
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        passenger = Passenger.objects.create(user=user, **validated_data)
        return passenger

    # TODO: test if it updates correctly
    def update(self, instance, validated_data):
            instance.credit_card = validated_data.get('credit_card')
            instance.save()

            nested_serializer = self.fields['user']
            nested_instance = instance.user
            # note the data is `pop`ed
            nested_data = validated_data.pop('user')
            nested_serializer.update(nested_instance, nested_data)
            # this will not throw an exception,
            # as `profile` is not part of `validated_data`
            return instance

    # def update(self, instance, validated_data):
    #     instance.credit_card = validated_data.get('credit_card')
    #     instance.save()

    #     user_data = validated_data.get('user', None)
    #     if user_data:
    #         username = user_data.get('username')
    #         user = User.objects.get(username=username)
    #         user.username = user_data.get('username', user.username)
    #         user.email = user_data.get('email', user.email)
    #         user.profile_picture = user_data.get('profile_picture', user.profile_picture)
    #         password = user_data.get('password', user.password)
    #         user.set_password(password)
    #         user.save()
    #         return user
    #     else:
    #         raise Exception("Missing field 'user'.")

# class DriverSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.StringRelatedField(queryset=User.objects.all())
#     class Meta:
#         model = Passenger
#         fields = ['credit_card', 'user']
