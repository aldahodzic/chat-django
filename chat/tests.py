from django.test import TransactionTestCase, TestCase, Client
from datetime import datetime

from .models import User, Message
from .encoders import encode_message, encode_messages, encode_user

client = Client()

class EncodersTest(TestCase):
  fixtures = ['user_messages.json']

  def test_encode_user(self):
    response = client.get('/users/1')
    expected = b'{"id": 1, "name": "John"}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)


  def test_encode_message(self):
    response = client.get('/messages/1')
    expected = b'{"id": 1, "body": "Hi Sally", "time_sent": "2022-02-22T01:25:57Z", "is_read": false, "sender": {"id": 1, "name": "John"}, "recipient": {"id": 2, "name": "Sally"}}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)


  def test_encode_messages(self):
    response = client.get('/messages')
    expected = b'{"messages": [{"id": 1, "body": "Hi Sally", "time_sent": "2022-02-22T01:25:57Z", "is_read": false, "sender": {"id": 1, "name": "John"}, "recipient": {"id": 2, "name": "Sally"}}, {"id": 2, "body": "Hello John, how are you?", "time_sent": "2022-02-22T01:26:16Z", "is_read": false, "sender": {"id": 2, "name": "Sally"}, "recipient": {"id": 1, "name": "John"}}]}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)
