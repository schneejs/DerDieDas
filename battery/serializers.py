from rest_framework import serializers
from battery.models import Battery


class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = ['user', 'card', 'level', 'last_modified']