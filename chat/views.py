from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import pbkdf2, get_random_string
import json

from .models import Message, User
from .encoders import encode_message, encode_messages, encode_user, encode_users

@method_decorator(csrf_exempt, name='dispatch')
class Messages(View):
  def get(self, request):
    return JsonResponse({
      'messages': encode_messages(Message.objects.all())
    })

  def post(self, request):
    message = Message(
      recipient=get_object_or_404(User, id=request.POST.get('recipient', False)),
      sender=get_object_or_404(User, id=request.POST.get('sender', False)),
      body=request.POST.get('body', False)
    )
    message.save()

    return HttpResponse(status=201)


@method_decorator(csrf_exempt, name='dispatch')
class Users(View):
  def get(self, request):
    return JsonResponse({
      'users': encode_users((User.objects.all()))
    })

  def post(self, request):
    salt = get_random_string()
    iterations = 10000
    hash = pbkdf2(
      request.POST.get('password'),
      get_random_string(),
      iterations
      )

    hash_string = "pbkdf2" + str(iterations) + salt + str(hash)

    user = User(
      name=request.POST.get('name'),
      hash=hash_string
    )
    user.save()

    return HttpResponse(status=201)

def message_by_id(request, message_id):
  message = encode_message(get_object_or_404(Message, id=message_id))
  return JsonResponse(message)

def user_by_id(request, user_id):
  user = encode_user(get_object_or_404(User, id=user_id))
  return JsonResponse(user)

def message_form(request, user_id):
  user = get_object_or_404(User, id=user_id)
  return render(request, "chat/send.html", {'user': user})

