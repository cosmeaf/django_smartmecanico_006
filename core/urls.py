from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ROUTES Custom Manager
from dashboard.views.address_view import AddressModelViewSet
from dashboard.views.vehicle_view import VehicleModelViewSet
from dashboard.views.user_view import CustomUserModelViewSet
from dashboard.views.services_view import ServiceModelViewSet, HourServiceModelViewSet



# Default Route Custom Manager
router = DefaultRouter()
router.register(r'users', CustomUserModelViewSet, basename='users')
router.register(r'addresses', AddressModelViewSet, basename='addresses')
router.register(r'vehicles', VehicleModelViewSet, basename='vehicles')
router.register(r'service', ServiceModelViewSet, basename='service')
router.register(r'hourservice', HourServiceModelViewSet, basename='hourservice')


urlpatterns = [
   path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('api-auth/', include('rest_framework.urls')),
   path('api/', include((router.urls))),
   path('api/', include('dashboard.urls')),
   path('', include('web.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)