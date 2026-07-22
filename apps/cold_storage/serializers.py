from rest_framework import serializers
from .models import ColdRoom


class ColdRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColdRoom
        fields = '__all__'
