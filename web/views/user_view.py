from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from dashboard.models.user_model import CustomUser
from dashboard.serializers.user_serializers import CustomUserSerializer, CustomUserDetailSerializer, CustomUserAllSerializer


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

    @action(detail=True, methods=['get'], renderer_classes=[renderers.JSONRenderer])
    def all_data(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserAllSerializer(user)
        return Response(serializer.data)
