from rest_framework import serializers
from dashboard.models.user_model import CustomUser
from dashboard.models.vehicle_model import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'fuel', 'year', 'odometer', 'plate', 'user']
        read_only_fields = ('id',)

class VehicleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'fuel', 'year', 'odometer', 'plate', 'user']
        read_only_fields = ('id', 'user')