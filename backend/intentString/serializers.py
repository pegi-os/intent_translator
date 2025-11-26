from rest_framework.serializers import ModelSerializer
from .models import IntentString

class IntentStringSerializer(ModelSerializer):
      class Meta:
            model = IntentString
            fields = ['user', 'intent', 'timestamp']