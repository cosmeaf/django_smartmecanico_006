from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from dashboard.models.user_model import CustomUser

class CustomRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8)],
    )
    passconf = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("O email já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passconf = cleaned_data.get("passconf")

        if password and passconf and password != passconf:
            self.add_error("passconf", "As senhas não coincidem.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
