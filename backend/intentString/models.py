from django.db import models

# Create your models here.
class IntentString(models.Model):
      user = models.CharField(max_length=20)
      intent = models.CharField(max_length=50)
      timestamp = models.DateTimeField()

      def __str__(self):
            return self.user + ":" + self.intent