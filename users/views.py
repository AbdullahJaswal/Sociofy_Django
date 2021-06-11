from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated, AllowAny

# ------ NO THROTTLING APPLIED ON LOGIN ------ APPLY IN FUTURE

permission = IsAuthenticated  # Change this to IsAuthenticated


# Create your views here.
class CustomUserCreate(APIView):
    throttle_scope = 'sign_up'  # Scoped throttle for special case. (Sign Up RATE)

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)

        if reg_serializer.is_valid():
            user = reg_serializer.save()

            if user:
                return Response(status=status.HTTP_201_CREATED)

            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    throttle_classes = [UserRateThrottle]  # Can only logout when logged in. (USER RATE)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    permission_classes = [permission]
    throttle_classes = [UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
