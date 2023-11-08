from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from dashboard.models.vehicle_model import Vehicle
from dashboard.serializers.vehicle_serializers import VehicleSerializer, VehicleDetailSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser

class WebVehicleModelViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return VehicleDetailSerializer
        return VehicleSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'vehicles': response.data}, template_name='dashboard/vehicle_list.html')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'vehicle': response.data}, template_name='dashboard/vehicle_detail.html')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response({'vehicle': response.data}, template_name='dashboard/vehicle_detail.html')
        return Response({'errors': response.data}, template_name='dashboard/vehicle_form.html')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'vehicle': response.data}, template_name='dashboard/vehicle_detail.html')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Veículo deletado'}, template_name='dashboard/vehicle_confirm_delete.html')
