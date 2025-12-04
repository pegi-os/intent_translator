from django.db import models

# Create your models here.
class NaturalIntent(models.Model):
      user = models.CharField(max_length=20)
      intent = models.CharField(max_length=300)
      timestamp = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.user + ":" + self.intent
      

class NetworkIntent(models.Model):
      name = models.CharField(max_length=100, null=True, blank=True)
      mac_address = models.CharField(max_length=17, null=True, blank=True)

      ipv4_start = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
      ipv4_end = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
      ipv6_start = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
      ipv6_end = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)

      timestamp = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.name + "/" + self.mac_address + self.ipv4_start + "~" + self.ipv4_end + "/" + self.ipv6_start + "~" + self.ipv6_end

class IntentInference(models.Model):
      # Intent
      intent_action = models.CharField(max_length=255, null=True, blank=True)
      intent_expectation_object = models.CharField(max_length=255, null=True, blank=True)
      intent_expectation_target = models.CharField(max_length=255, null=True, blank=True)

      # KGTriple
      kg_head = models.CharField(max_length=255, null=True, blank=True)
      kg_relation = models.CharField(max_length=255, null=True, blank=True)
      kg_tail = models.CharField(max_length=255, null=True, blank=True)

      # 옵션
      confidence = models.FloatField(null=True, blank=True)
      degraded = models.BooleanField(default=False)
      degradation_note = models.TextField(null=True, blank=True)

      # 타임스탬프
      timestamp = models.DateTimeField()

      # FK
      natural_intent = models.ForeignKey(NaturalIntent, null=True, blank=True, on_delete=models.CASCADE)
      network_intent = models.ForeignKey(NetworkIntent, null=True, blank=True, on_delete=models.CASCADE)

      class Meta:
            ordering = ["-timestamp"]

      def __str__(self):
            return f"IntentRecord #{self.pk}"