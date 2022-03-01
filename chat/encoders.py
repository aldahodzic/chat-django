
def encode_user(user):
  return {
    'id': user.id,
    'name': user.name
  }

def encode_users(users):
  return [encode_user(user) for user in users]


def encode_message(message):
  return {
    'id': message.id,
    'body': message.body,
    'time_sent': message.time_sent,
    'is_read': message.is_read,
    'sender': encode_user(message.sender),
    'recipient': encode_user(message.recipient)
  }


def encode_messages(messages):
  return [encode_message(message) for message in messages]
