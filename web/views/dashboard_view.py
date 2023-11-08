from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models.user_model import CustomUser
from dashboard.models.address_model import Address
from dashboard.models.vehicle_model import Vehicle
import logging

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['page_title'] = 'Dashboard'
        context['screen_name'] = 'Dashboard'
        context['user'] = user
        context['addresses'] = user.address.all()
        context['vehicles'] = user.vehicles.all()
        return context
