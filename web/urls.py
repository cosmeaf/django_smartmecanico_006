from django.urls import path
from django.contrib.auth import views as auth_views
from .views.login_view import CustomLoginView
from .views.register_view import CustomRegisterView
from .views.password_recovery_view import CustomPasswordRecoveryView
from .views.home_view import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('password-recovery/', CustomPasswordRecoveryView.as_view(), name='password_recovery'),
    # path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

