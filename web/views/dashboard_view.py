from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models.user_model import CustomUser
from dashboard.serializers.user_serializers import CustomUserSerializer, CustomUserDetailSerializer, CustomUserAllSerializer

import logging

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'dashboard/index.html'
    context_object_name = 'user'

    def get_object(self):
        # Garante que estamos pegando o objeto do usuário logado
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Utiliza o serializer para obter os dados serializados do usuário
        context['page_title'] = 'Dashboard'
        context['screen_name'] = 'Dashboard'
        serializer = CustomUserAllSerializer(user)
        context['user_data'] = serializer.data
        return context
