from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import IntentStringSerializer
from .models import IntentString

# Create your views here.
def test(request):
      return HttpResponse("Test")

class IntentStringViewSet(viewsets.ModelViewSet):
      queryset = IntentString.objects.all()
      serializer_class = IntentStringSerializer