from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)

from .users.serializers import UserSerializer

class MyTokenObtainPairSerializer(
    TokenObtainPairSerializer
):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.pk
        return data
