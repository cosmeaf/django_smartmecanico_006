from django.urls import reverse
from django.http import JsonResponse
from web.forms.auth_user_recovery_form import AuthUserRecoveryForm
from django.views.generic.edit import FormView

class CustomPasswordRecoveryView(FormView):
    template_name = 'registration/password_recovery.html'
    form_class = AuthUserRecoveryForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # Verifique se é uma solicitação AJAX usando o cabeçalho HTTP_X_REQUESTED_WITH
        is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if form.is_valid():
            # A lógica da solicitação de recuperação de senha já foi tratada no formulário.
            # Você pode adicionar qualquer ação de resposta necessária aqui.
            if is_ajax_request:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitação enviada com sucesso.'
                })
            else:
                # Lógica de resposta não-AJAX (redirecionamento, por exemplo)
                # Adicione sua lógica de redirecionamento aqui, se necessário.
                pass
        else:
            # O formulário já tratou a validação e os erros, então não é necessário fazer nada aqui.
            if is_ajax_request:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors,
                    'message': 'Erros de validação.'
                }, status=400)

        return super().post(request, *args, **kwargs)
