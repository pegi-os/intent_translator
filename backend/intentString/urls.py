from django.urls import path
from . import views

urlpatterns = [
      path('test_api', views.test, name='nametest')
]