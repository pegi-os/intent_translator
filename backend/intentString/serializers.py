from rest_framework.serializers import ModelSerializer
from .models import NaturalIntent, NetworkIntent, PolicyIntent

class NaturalIntentSerializer(ModelSerializer):
      class Meta:
            model = NaturalIntent
            fields = ['user', 'intent', 'timestamp']

class NetworkIntentSerializer(ModelSerializer):
      class Meta:
            model = NetworkIntent
            fields = '__all__'

class PolicyIntentSerializer(ModelSerializer):
    class Meta:
        model = PolicyIntent
        fields = '__all__'
