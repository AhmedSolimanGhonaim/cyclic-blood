from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import ListAPIView , RetrieveAPIView
from .serializers import CustomUserSerializer, RegistrationSerializer, MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import AllowAny, IsAuthenticated , IsAdminUser
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "User registration endpoint"}, status=status.HTTP_200_OK)
    def post(self,request ):
         serializer = RegistrationSerializer(data=request.data)
         if serializer.is_valid():
               user = serializer.save()
               return Response({"message": "User registered successfully", "user_id": user.id}, status=201)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSett(ModelViewSet):
     queryset = CustomUser.objects.all()
     serializer_class = CustomUserSerializer
     
     
     def get_permissions(self):
         if self.action == 'me':
                return [IsAuthenticated()]
         elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
                return [IsAdminUser()]

         return super().get_permissions()
     @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
     def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)