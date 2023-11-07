from django.urls import reverse
from django.http import JsonResponse
from web.forms.user_register_form import CustomRegisterForm
from django.views.generic.edit import FormView

class CustomRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomRegisterForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if form.is_valid():
            user = form.save()
            if user and is_ajax_request:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Registration successful.',
                    'redirect_url': reverse('login')
                })
        else:
            errors = {field: errors for field, errors in form.errors.items()}
            if is_ajax_request:
                return JsonResponse({
                    'status': 'error',
                    'errors': errors,
                    'message': 'Validation errors.'
                }, status=400)

        return super().post(request, *args, **kwargs)
