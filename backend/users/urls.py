from django.urls import path

from .views import RegisterView, VerifyOtpView, LoginView, ResendOtpView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView, ProfileView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("resend-otp/", ResendOtpView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view()),
    path("profile/", ProfileView.as_view()),
]
