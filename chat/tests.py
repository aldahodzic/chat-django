from django.test import TransactionTestCase, TestCase, Client, override_settings
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import json


from .models import  Message
from .encoders import encode_message, encode_messages, encode_user

client = Client()

class EncoderTests(TestCase):
  fixtures = ['user_messages.json']


  def test_encode_users(self):
    response = client.get('/users')
    expected = b'{"users": [{"id": 1, "username": "brandon", "email": "contact@brandonmurch.com"}, {"id": 2, "username": "Bob", "email": "Bob@email.com"}]}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)

  def test_encode_user(self):
    response = client.get('/users/1')
    expected = b'{"id": 1, "username": "brandon", "email": "contact@brandonmurch.com"}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)


  def test_encode_message(self):
    response = client.get('/messages/1')
    expected = b'{"id": 1, "body": "Hi Sally", "time_sent": "2022-02-22T01:25:57Z", "is_read": false, "sender": {"id": 1, "username": "brandon", "email": "contact@brandonmurch.com"}, "recipient": {"id": 2, "username": "Bob", "email": "Bob@email.com"}}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)


  def test_encode_messages(self):
    response = client.get('/messages')
    expected = b'{"messages": [{"id": 1, "body": "Hi Sally", "time_sent": "2022-02-22T01:25:57Z", "is_read": false, "sender": {"id": 1, "username": "brandon", "email": "contact@brandonmurch.com"}, "recipient": {"id": 2, "username": "Bob", "email": "Bob@email.com"}}, {"id": 2, "body": "Hello John, how are you?", "time_sent": "2022-02-22T01:26:16Z", "is_read": false, "sender": {"id": 2, "username": "Bob", "email": "Bob@email.com"}, "recipient": {"id": 1, "username": "brandon", "email": "contact@brandonmurch.com"}}]}'

    self.assertEquals(200, response.status_code)
    self.assertEquals(expected, response.content)

class PostTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_message_post(self):
    message_count = len(Message.objects.all())

    new_message_json = '{"body": "Test Message", "sender": 2, "recipient": 1}'
    response = client.post('/messages', new_message_json, "application/json")

    self.assertEqual(201, response.status_code)

    # Ensure a message has been added.
    self.assertEquals(message_count + 1, len(Message.objects.all()))

    # Ensure the message has the correct fields.
    self.assertEqual(Message.objects.last().body, "Test Message")
    self.assertEqual(Message.objects.last().sender.id, 2)
    self.assertEqual(Message.objects.last().recipient.id, 1)

  def test_user_post(self):
    user_count = len(User.objects.all())

    new_user = '{"username": "Harry", "email": "harry@email.com", "password": "Test"}'
    response = client.post('/users', new_user, "application/json")

    self.assertEqual(201, response.status_code)

    # Ensure a user has been added.
    self.assertEquals(user_count + 1, len(User.objects.all()))

    # Ensure the new user has the correct name.
    self.assertEqual(User.objects.last().username, "Harry")

class PutTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_user_put(self):
      # Sanity test
      user = User.objects.get(id=1)
      self.assertEqual(user.username, "brandon")

      # Update user
      update_user = '{"username": "Sarah", "email": "sarah@email.com", "password": "Test"}'
      response = client.put('/users/1', update_user, "application/json")

      # Test response
      self.assertEqual(200, response.status_code)

      # Test user has been updated
      user = User.objects.get(id=1)
      self.assertNotEqual(user.username, "brandon")
      self.assertEqual(user.username, "Sarah")


class DeleteTests(TransactionTestCase):
  fixtures = ['user_messages.json']

  def test_message_delete(self):
    message_count = len(Message.objects.all())

    response = client.delete('/messages/1')

    self.assertEqual(200, response.status_code)
    self.assertEquals(message_count - 1, len(Message.objects.all()))

    self.assertRaises(ObjectDoesNotExist, lambda  : Message.objects.get(id=1))


  def test_user_delete(self):
      user_count = len(User.objects.all())

      response = client.delete('/users/1')

      self.assertEqual(200, response.status_code)
      self.assertEquals(user_count - 1, len(User.objects.all()))

      self.assertRaises(ObjectDoesNotExist, lambda  : User.objects.get(id=1))



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
