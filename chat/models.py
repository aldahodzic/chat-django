from django.db import models
from django.utils.timezone import now


class User(models.Model):
  name = models.CharField(max_length=50)
  hash = models.CharField(max_length=255)

  def __str__(self):
      return self.name


class Message(models.Model):
  body = models.CharField(max_length=255)
  time_sent = models.DateTimeField(default=now)
  is_read = models.BooleanField(default=False)
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sender")
  recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipient")
