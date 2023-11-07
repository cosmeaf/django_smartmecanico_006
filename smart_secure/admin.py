# secure/admin.py
from django.contrib import admin
from django.core.management import call_command
from .models import SSLCertificate
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

@admin.register(SSLCertificate)
class SSLCertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    ordering = ['created_at']
    autocomplete_fields = ['user']

    # Ações personalizadas para Admin
    change_list_template = "admin/ssl_certificate_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate_ssl/', self.admin_site.admin_view(self.generate_ssl), name='generate-ssl'),
        ]
        return custom_urls + urls

    def generate_ssl(self, request):
        # Aqui você chamaria o comando ssl_generate
        if 'apply' in request.POST:
            try:
                call_command('ssl-generate', web=True)
                self.message_user(request, "Certificado SSL gerado com sucesso.")
            except Exception as e:
                self.message_user(request, f'Erro ao gerar o certificado SSL: {e}', level='error')
            return HttpResponseRedirect("../")

        return render(request, "admin/ssl_generate.html")
