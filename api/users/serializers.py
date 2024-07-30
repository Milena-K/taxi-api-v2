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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # user = UserSerializer()
    class Meta:
        model = Passenger
        fields = ['credit_card', 'user']
        depth = 1

    # def update(self, instance, validated_data):
    #     instance.credit_card = validated_data.get('credit_card')
    #     instance.save()

    #     user_data = validated_data.get('user')
    #     user = User.objects.get(username=user_data.get('username'))
    #     user.username = user_data.get('username', user.username)
    #     user.email = user_data.get('email', user.email)
    #     user.profile_picture = user_data.get('profile_picture', user.profile_picture)


    # def create(self, validated_data):
    #     items = validated_data.pop('items', None)
    #     invoice = Invoice(**validated_data)
    #     invoice.save()
    #     for item in items:
    #         InvoiceItem.objects.create(invoice=invoice, **item)
    #     return invoice


    ##### example
    # items = validated_data.get('items')

    # for item in items:
    #     item_id = item.get('id', None)
    #     if item_id:
    #         inv_item = InvoiceItem.objects.get(id=item_id, invoice=instance)
    #         inv_item.name = item.get('name', inv_item.name)
    #         inv_item.price = item.get('price', inv_item.price)
    #         inv_item.save()
    #     else:
    #         InvoiceItem.objects.create(account=instance, **item)

    # return instance
# class DriverSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.StringRelatedField(queryset=User.objects.all())
#     class Meta:
#         model = Passenger
#         fields = ['credit_card', 'user']
