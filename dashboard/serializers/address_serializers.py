from rest_framework import serializers
from dashboard.models.address_model import Address
from dashboard.models.user_model import CustomUser

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())

    class Meta:
        model = Address
        fields = ['id', 'cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'user']
        read_only_fields = ('id', 'user')

    def validate_cep(self, value):
        """Valida se o CEP tem o formato correto."""
        if len(value) not in [8, 9]:
            raise serializers.ValidationError("CEP inválido. Certifique-se de que o CEP contém 8 dígitos.")
        return value

class AddressDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email',queryset=CustomUser.objects.all(),default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = ['id', 'cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'user']
        read_only_fields = ('id', 'user')

    def validate_cep(self, value):
        """Valida se o CEP tem o formato correto."""
        if len(value) not in [8, 9]:
            raise serializers.ValidationError("CEP inválido. Certifique-se de que o CEP contém 8 dígitos.")
        return value