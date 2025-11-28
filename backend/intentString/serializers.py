from rest_framework.serializers import ModelSerializer
from .models import NaturalIntent, NetworkIntent

class NaturalIntentSerializer(ModelSerializer):
      class Meta:
            model = NaturalIntent
            fields = ['user', 'intent', 'timestamp']

class NetworkIntentSerializer(ModelSerializer):
      class Meta:
            model = NetworkIntent
            fields = '__all__'