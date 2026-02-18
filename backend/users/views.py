from rest_framework import generics
from .models import User
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import ProfileSerializer, RegisterSerializer, VerifyOtpSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, VerifyOtpSerializer, LoginSerializer





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower()
        from .models import User
        from .services import send_email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  # Adjust for your frontend
        send_email("Password reset", f"Reset your password: {reset_link}", user.email)
        return Response({"detail": "Password reset link sent to email."})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        from .models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode
        password = request.data.get("password")
        if not password:
            return Response({"detail": "Password required."}, status=400)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid link."}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=400)
        user.set_password(password)
        user.save()
        return Response({"detail": "Password reset successful."})



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or expired token."}, status=400)
        return Response({"detail": "Logout successful."})





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


class ResendOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower()
        from .models import User, EmailOTP
        from .services import send_otp_email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        if user.is_active:
            return Response({"detail": "User already verified"}, status=400)
        code = EmailOTP.generate_code()
        EmailOTP.objects.create(
            user=user,
            code=code,
            expires_at=EmailOTP.expiry_time(minutes=1),
        )
        send_otp_email(user.email, code)
        return Response({"detail": "OTP resent to email"})




class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(s.validated_data)
