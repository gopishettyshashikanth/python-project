from rest_framework import serializers
from myapp.models import *

class AppointmentSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=60)

class CustomrtSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=60)    