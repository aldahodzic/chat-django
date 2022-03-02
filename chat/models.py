from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Message(models.Model):
  body = models.CharField(max_length=255, null=False)
  time_sent = models.DateTimeField(default=now, null=False)
  is_read = models.BooleanField(default=False, null=False)
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sender", null=False)
  recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipient", null=False)
