from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse, reverse_lazy
from dashboard.models.user_model import CustomUser


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('dashboard')
        else:
            return super().get_redirect_url()

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if user is not None:
            login(request, user)
            if is_ajax_request:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Logged in successfully.',
                    'redirect_url': reverse('dashboard')
                })
        else:
            if is_ajax_request:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email or password.'
                }, status=400)

        return super().post(request, *args, **kwargs)

    def get_users(request):
        users = CustomUser.objects.all()
        data = serializers.serialize('json', users)
        return JsonResponse({'users': data})

