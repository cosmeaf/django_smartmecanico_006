from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from dashboard.models.user_model import CustomUser
from dashboard.serializers.user_serializers import CustomUserSerializer, CustomUserDetailSerializer, CustomUserAllSerializer
import logging

logger = logging.getLogger(__name__)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user
    
class WebUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        self.serializer_class = CustomUserSerializer
        response = super(WebUserModelViewSet, self).list(request, *args, **kwargs)
        return Response({'users': response.data}, template_name='dashboard/user_list.html')

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CustomUserAllSerializer
        response = super(WebUserModelViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'user': response.data}, template_name='dashboard/user_detail.html')

    def create(self, request, *args, **kwargs):
        self.serializer_class = CustomUserSerializer
        response = super(WebUserModelViewSet, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            return Response({'user': response.data}, template_name='dashboard/user_detail.html')
        return Response({'errors': response.data}, template_name='dashboard/user_form.html')

    def update(self, request, *args, **kwargs):
        self.serializer_class = CustomUserDetailSerializer
        response = super(WebUserModelViewSet, self).update(request, *args, **kwargs)
        return Response({'user': response.data}, template_name='dashboard/user_detail.html')

    def destroy(self, request, *args, **kwargs):
        response = super(WebUserModelViewSet, self).destroy(request, *args, **kwargs)
        return Response({'message': 'Usuário deletado'}, template_name='dashboard/user_confirm_delete.html')

    @action(detail=True, methods=['get'], renderer_classes=[renderers.TemplateHTMLRenderer])
    def all_data(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            custom_user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserAllSerializer(custom_user)
            logger.error(f'USER DATA ALL {serializer.data}')
            return Response({'detail': serializer.data}, template_name='dashboard/user_detail.html')
        except CustomUser.DoesNotExist:
            logger.error(f'User with pk {pk} does not exist.')
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

