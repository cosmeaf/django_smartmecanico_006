from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from dashboard.models.address_model import Address
from dashboard.serializers.address_serializers import AddressSerializer, AddressDetailSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser

class WebAddressModelViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return AddressDetailSerializer
        return AddressSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'addresses': response.data}, template_name='dashboard/address_list.html')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'address': response.data}, template_name='dashboard/address_detail.html')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response({'address': response.data}, template_name='dashboard/address_detail.html')
        return Response({'errors': response.data}, template_name='dashboard/address_form.html')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'address': response.data}, template_name='dashboard/address_detail.html')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Endereço deletado'}, template_name='dashboard/address_confirm_delete.html')
