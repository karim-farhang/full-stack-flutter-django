from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailOTP
from .services import send_otp_email

User = get_user_model()



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def create(self, validated_data):
        email = validated_data["email"].lower()
        user = User(
            email=email,
            username=validated_data["username"],
            is_active=False,  # important: inactive until OTP verified
        )
        user.set_password(validated_data["password"])
        user.save()

        code = EmailOTP.generate_code()
        EmailOTP.objects.create(
            user=user,
            code=code,
            expires_at=EmailOTP.expiry_time(minutes=5),
        )
        send_otp_email(user.email, code)
        return user


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        email = attrs["email"].lower()
        code = attrs["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        otp = (
            EmailOTP.objects.filter(user=user, code=code, is_used=False)
            .order_by("-created_at")
            .first()
        )
        if not otp:
            raise serializers.ValidationError("Invalid OTP")
        if otp.is_expired():
            raise serializers.ValidationError("OTP expired")

        attrs["user"] = user
        attrs["otp"] = otp
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        otp = validated_data["otp"]

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        user.is_active = True
        user.save(update_fields=["is_active"])

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            # resend OTP automatically
            code = EmailOTP.generate_code()
            EmailOTP.objects.create(
                user=user,
                code=code,
                expires_at=EmailOTP.expiry_time(minutes=5),
            )
            send_otp_email(user.email, code)
            raise serializers.ValidationError("Account not verified. OTP resent.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "avatar"]
        read_only_fields = ["id", "email"]

