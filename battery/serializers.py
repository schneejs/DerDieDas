from rest_framework import serializers
from battery.models import Battery


class UserBatteriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = ['card', 'level', 'last_modified']