from django.contrib import admin
from django import forms
from django.shortcuts import render
from dashboard.models.vehicle_model import Vehicle
from dashboard.models.user_model import CustomUser

class VehicleAdminForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise forms.ValidationError('É necessário selecionar um usuário.')
        return user

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    form = VehicleAdminForm
    list_display = ('plate', 'brand', 'model', 'year', 'user_column')
    list_filter = ('plate', 'brand', 'model', 'year', 'user')
    search_fields = ('brand', 'model', 'year', 'plate', 'user__email')
    list_display_links = ('plate', 'user_column',)
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    autocomplete_fields = ['user']

    def user_column(self, instance):
        return instance.user.email if instance.user else '-'
    user_column.short_description = 'User'


    def get_queryset(self, request):
        queryset = super(VehicleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_id=request.user.id)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser and form.cleaned_data.get('user'):
            obj.user = form.cleaned_data.get('user')
        super().save_model(request, obj, form, change)

    def change_owner(self, request, queryset):
        users = CustomUser.objects.all()  # Use CustomUser em vez de User
        return render(request, 'admin/change_owner.html', {'users': users, 'queryset': queryset})
    change_owner.short_description = "Change owner of selected vehicles"

    def select_all_vehicles(self, request, queryset):
        queryset.update(selected=True)
    select_all_vehicles.short_description = "Select all vehicles"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions