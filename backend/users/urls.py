from django.urls import path
from .views import RegisterView, VerifyOtpView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("login/", LoginView.as_view()),
]
