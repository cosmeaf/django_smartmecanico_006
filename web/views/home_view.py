from django.views import generic
from django.shortcuts import render
from dashboard.models.testimonial_model import Testimonial
from django.db.models import F

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.order_by('?')[:3]
        return context
