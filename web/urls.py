from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views.home_view import HomeView
from web.views.dashboard_view import DashboardView
from rest_framework.routers import DefaultRouter

app_name = 'web'

# ROUTES WEB 
from web.views.user_view import WebUserModelViewSet
from web.views.address_view import WebAddressModelViewSet
from web.views.vehicle_view import WebVehicleModelViewSet
from web.views.appointment_view import WebAppointmentModelViewSet

# Default Route web
router = DefaultRouter()
router.register(r'users', WebUserModelViewSet, basename='users')
router.register(r'address', WebAddressModelViewSet, basename='address')
router.register(r'vehicle', WebVehicleModelViewSet, basename='vehicle')
router.register(r'appointment', WebAppointmentModelViewSet, basename='appointment')


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('dashboard/', include((router.urls))),
    path('dashboard/users/<uuid:pk>/all_data/', WebUserModelViewSet.as_view({'get': 'all_data'}), name='users-all-data'),

]


