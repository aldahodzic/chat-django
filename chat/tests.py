from django.test import TransactionTestCase, TestCase, Client
from datetime import datetime

from .models import User, Message
from .encoders import encode_message, encode_messages, encode_user

client = Client()

class EncoderTests(TestCase):
  fixtures = ['user_messages.json']


  def test_encode_users(self):
    response = client.get('/users')
    expected = b'{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Sally"}]}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)

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

class MessagesPostTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_message_post(self):
    message_count = len(Message.objects.all())

    new_message = {"body": "Test Message", "sender": 2, "recipient": 1}
    response = client.post('/messages', new_message)

    self.assertEqual(201, response.status_code)
    self.assertEquals(message_count + 1, len(Message.objects.all()))

    get_response = client.get('/messages')
    self.assertContains(get_response, "Test Message")


  def test_user_post(self):
    user_count = len(User.objects.all())

    new_user = {"name": "Harry", "password": "Test"}
    response = client.post('/users', new_user)

    self.assertEqual(201, response.status_code)
    self.assertEquals(user_count + 1, len(User.objects.all()))

    get_response = client.get('/users')
    self.assertContains(get_response, "Harry")



class MessagesDeleteTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_message_delete(self):
    message_count = len(Message.objects.all())

    response = client.delete('/messages/1')

    self.assertEqual(200, response.status_code)
    self.assertEquals(message_count - 1, len(Message.objects.all()))

    get_response = client.get('/messages')
    self.assertNotContains(get_response, "Hi Sally")


  def test_user_delete(self):
      user_count = len(User.objects.all())

      response = client.delete('/users/1')

      self.assertEqual(200, response.status_code)
      self.assertEquals(user_count - 1, len(User.objects.all()))

      get_response = client.get('/users')
      self.assertNotContains(get_response, "John")
