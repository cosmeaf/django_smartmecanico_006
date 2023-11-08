from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from dashboard.models.appointment_model import Appointment
from dashboard.serializers.appointment_serializers import AppointmentSerializer, AppointmentDetailSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser

class WebAppointmentModelViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return AppointmentDetailSerializer
        return AppointmentSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'appointments': response.data}, template_name='dashboard/appointment_list.html')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'appointment': response.data}, template_name='dashboard/appointment_detail.html')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response({'appointment': response.data}, template_name='dashboard/appointment_detail.html')
        return Response({'errors': response.data}, template_name='dashboard/appointment_form.html')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({'appointment': response.data}, template_name='dashboard/appointment_detail.html')
        return Response({'errors': response.data}, template_name='dashboard/appointment_form.html')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Agendamento deletado'}, template_name='dashboard/appointment_confirm_delete.html')
