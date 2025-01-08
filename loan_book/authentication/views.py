# authentication/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from django.contrib.auth import get_user_model


class RegisterUserView(APIView):
    """
    Register a new user (automatically assigned as a creditor).
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    Login a user and return JWT tokens (access and refresh).
    """

    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone_number or not password:
            return Response({"error": "Phone_number and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(phone_number=phone_number)
        except get_user_model().DoesNotExist:
            return Response({"error": "Invalid phone_number or password"}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token,
                "refresh": str(refresh),
            })

        return Response({"error": "Invalid phone_number or password"}, status=status.HTTP_400_BAD_REQUEST)
