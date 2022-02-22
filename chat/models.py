from django.db import models


class User(models.Model):
  name = models.CharField(max_length=50)
  hash = models.CharField(max_length=255)

  def __str__(self):
      return self.name


# Create your models here.
class Message(models.Model):
  body = models.CharField(max_length=255)
  time_sent = models.DateTimeField()
  is_read = models.BooleanField()
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sender")
  recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipient")
