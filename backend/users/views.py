from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, VerifyOtpSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"detail": "OTP sent to email"}, status=status.HTTP_201_CREATED)

class VerifyOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = VerifyOtpSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        tokens = s.save()
        return Response(tokens)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(s.validated_data)
