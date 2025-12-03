from django.db import models

# Create your models here.
class NaturalIntent(models.Model):
      user = models.CharField(max_length=20)
      intent = models.CharField(max_length=50)
      timestamp = models.DateTimeField()

      def __str__(self):
            return self.user + ":" + self.intent
      

class NetworkIntent(models.Model):
      name = models.CharField(max_length=100, null=True, blank=True)
      mac_address = models.CharField(max_length=17, null=True, blank=True)

      ipv4_start = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
      ipv4_end = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
      ipv6_start = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
      ipv6_end = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
      

      def __str__(self):
            return self.name + "/" + self.mac_address + self.ipv4_start + "~" + self.ipv4_end + "/" + self.ipv6_start + "~" + self.ipv6_end

class PolicyIntent(models.Model):
    action = models.CharField(max_length=100)
    expectation_object = models.CharField(max_length=200)
    expectation_target = models.CharField(max_length=200)

    head = models.CharField(max_length=200)
    relation = models.CharField(max_length=200)
    tail = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
