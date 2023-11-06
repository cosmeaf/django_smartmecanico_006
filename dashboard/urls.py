from django.urls import path
from dashboard.views.authentication_view import AuthUserRegisterView, AuthUserSignInView, AuthUserRecoveryView, AuthUserOtpView, AuthUserResetPasswordView

urlpatterns = [
    path('register/', AuthUserRegisterView.as_view(), name='register'),
    path('signin/', AuthUserSignInView.as_view(), name='signin'),
    path('recovery/', AuthUserRecoveryView.as_view(), name='recovery'),
    path('otp/', AuthUserOtpView.as_view(), name='otp'),
    path('reset-password/<uuid:uuid>/<str:token>/', AuthUserResetPasswordView.as_view(), name='reset-password'),
]