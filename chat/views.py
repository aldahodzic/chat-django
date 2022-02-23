from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import json

from .models import Message, User
from .encoders import encode_message, encode_messages

def messages(request):
  if request.method == "GET":
    return JsonResponse({
      'messages': encode_messages(Message.objects.all())
    })

  if request.method == "POST":
    message = Message(
      recipient=get_object_or_404(User, name=request.POST['recipient']),
      sender=get_object_or_404(User, id=request.POST['sender']),
      body=request.POST['body']
    )
    message.save()

    return HttpResponseRedirect(reverse('chat:messages'))

def message_by_id(request, message_id):
  message = encode_message(get_object_or_404(Message, id=message_id))
  return JsonResponse(message)


def message_form(request, user_id):
  user = get_object_or_404(User, id=user_id)
  return render(request, "chat/send.html", {'user': user})

