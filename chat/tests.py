from django.test import TransactionTestCase, TestCase, Client, override_settings
from datetime import datetime
import json

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

class PostTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_message_post(self):
    message_count = len(Message.objects.all())

    new_message = json.loads('{"body": "Test Message", "sender": 2, "recipient": 1}')
    response = client.post('/messages', new_message, "application/json")

    self.assertEqual(201, response.status_code)
    self.assertEquals(message_count + 1, len(Message.objects.all()))

    get_response = client.get('/messages')
    self.assertContains(get_response, "Test Message")


  def test_user_post(self):
    user_count = len(User.objects.all())

    new_user = json.loads('{"name": "Harry", "password": "Test"}')
    response = client.post('/users', new_user, "application/json")

    self.assertEqual(201, response.status_code)
    self.assertEquals(user_count + 1, len(User.objects.all()))

    get_response = client.get('/users')
    self.assertContains(get_response, "Harry")


class PutTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_user_put(self):
      get_response = client.get('/users/1')
      self.assertContains(get_response, "John")
      # self.assertContains(get_response, '"hash": ""')

      update_user = '{"name": "Sarah","password": "Test"}'
      response = client.put('/users/1', update_user, "application/json")

      self.assertEqual(200, response.status_code)

      get_response = client.get('/users/1')
      self.assertNotContains(get_response, "John")
      # self.assertNotContains(get_response, '"hash": ""')
      self.assertContains(get_response, "Sarah")


class DeleteTests(TransactionTestCase):
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


@override_settings(MIDDLEWARE=['chat.middleware.requestmiddleware.json_middleware'])
class JsonMiddlewareTests(TestCase):

  def test_plain_text(self):
    new_user = '{"name": "Harry", "password": "Test"}'
    response = client.post('/users', new_user, "text/plain")

    self.assertEqual(415, response.status_code)


  def test_malformed_json(self):
    # Missing comma in between attributes.
    new_user = '{"name": "Harry" "password": "Test"}'
    response = client.post('/users', new_user, "application/json")

    self.assertEqual(400, response.status_code)
