from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer, MyTokenObtainPairSerializer,  PassengerSerializer
from .models import Passenger

User = get_user_model()

# list, get user by ID, edit user by ID
class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all() # TODO: add order_by()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # TODO: change to IsAdminOnly


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


class PassengerViewSet(ViewSet):
    """
    API endpoint for handling passenger data
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request: Request):
        serializer = PassengerSerializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        data = JSONParser().parse(request)
        passenger_serializer = PassengerSerializer(data=data)
        if passenger_serializer.is_valid():
            passenger_serializer.save()
            return Response(data=passenger_serializer.data, status=status.HTTP_200_OK)
        return Response(data=passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # this create method is with the permission.IsAuthenticated
    # def create(self, request: Request):
    #     data = JSONParser().parse(request)
    #     user_serializer = UserSerializer(request.user)
    #     username = user_serializer.data.pop("username")
    #     user = User.objects.get(username=username)
    #     data["user"] = user.__dict__
    #     passenger_serializer = PassengerSerializer(data=data)
    #     if passenger_serializer.is_valid():
    #          passenger_serializer.save()
    #          return Response(data=passenger_serializer.data, status=status.HTTP_200_OK)
    #     return Response(data=passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        GET method for getting information
        about a specific passenger.

        url /passengers/1/
        """
        if pk:
            try:
                user = User.objects.get(pk=pk)
                passenger = Passenger.objects.get(user=user)
                serializer = PassengerSerializer(passenger)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(data={"message": "There is no passenger with this pk"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """
        PATCH method for partially updating passenger info

        url /passengers/1/
        """
        user = User.objects.get(pk=pk)
        passenger = Passenger.objects.get(user=user)
        serializer = PassengerSerializer(passenger, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)




#     def partial_update(self, request, pk=None):
        # """ PATCH method """
#         pass

#     def destroy(self, request, pk=None):
#         pass
