from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all() # TODO: add order_by()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
