from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer, MyTokenObtainPairSerializer

User = get_user_model()

# list, get user by ID, edit user by ID
class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all() # TODO: add order_by()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
