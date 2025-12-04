from rest_framework.serializers import ModelSerializer
from .models import NaturalIntent, NetworkIntent, IntentInference

class NaturalIntentSerializer(ModelSerializer):
      class Meta:
            model = NaturalIntent
            fields = ['user', 'intent', 'timestamp']

class NetworkIntentSerializer(ModelSerializer):
      class Meta:
            model = NetworkIntent
            fields = '__all__'

class IntentInferenceSerializer(ModelSerializer):
      class Meta:
            model = IntentInference
            fields = '__all__'