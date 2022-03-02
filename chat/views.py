from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import json

from .models import Message
from .encoders import encode_message, encode_messages, encode_user, encode_users

@method_decorator(csrf_exempt, name='dispatch')
class Messages(LoginRequiredMixin, View):
  raise_exception=True

  def get(self, request):
    return JsonResponse({
      'messages': encode_messages(Message.objects.all())
    })

  def post(self, request):
    message = Message(
      recipient=request.user,
      sender=get_object_or_404(User, id=request.json.get('sender', False)),
      body=request.json.get('body', False)
    )
    message.save()

    return HttpResponse(status=201)


@method_decorator(csrf_exempt, name='dispatch')
class Users(LoginRequiredMixin, View):
  raise_exception=True

  def get(self, request):
    return JsonResponse({
      'users': encode_users((User.objects.all()))
    })

  def post(self, request):
    user = User.objects.create(
      username=request.json.get('username'),
      email=request.json.get('email'),
      password=make_password(request.json.get('password'))
    )
    user.save()

    return HttpResponse(status=201)

@method_decorator(csrf_exempt, name='dispatch')
class MessageById(LoginRequiredMixin, View):
  raise_exception=True

  def get(self, request, message_id):
    message = encode_message(get_object_or_404(Message, id=message_id))
    return JsonResponse(message)

  def put(self, request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if (request.json.get("is_read")):
      message.is_read = request.json.get("is_read")

    message.save()

    return HttpResponse(status=200)

  def delete(self, request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UserById(LoginRequiredMixin, View):
  raise_exception=True

  def get(self, request, user_id):
    user = encode_user(get_object_or_404(User, id=user_id))
    return JsonResponse(user)

  def put(self, request, user_id):
    user = get_object_or_404(User, id=user_id)

    if (request.json.get("username")):
      user.username = request.json.get("username")

    if (request.json.get("password")):
      if (len(user.password.split("$")) == 4):
        user.hash = make_password(
          request.json.get("password"),
          user.password.split("$")[2]
        )
      else:
        user.hash = make_password(
          request.json.get("password"),
        )

    user.save()

    return HttpResponse(status=200)

  def delete(self, request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class Authenticate(View):
  def get(self, request):
    if request.user.is_authenticated:
      return HttpResponse(status=200)
    else:
      return HttpResponse(status=403)

  def post(self, request):
    user = authenticate(request, username=request.json.get('username'), password=request.json.get('password'))

    print(user)

    if user is not None:
      login(request, user)
      return HttpResponse(status=200)
    else:
      return HttpResponse(status=403)

  def delete(self, request):
    logout(request)

    return HttpResponse(status=200)



def message_form(request, user_id):
  user = get_object_or_404(User, id=user_id)
  return render(request, "chat/send.html", {'user': user})

