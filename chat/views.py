from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.serializers import serialize
import json

from .models import Message, User
from .encoders import DateEncoder

# Create your views here.

def hello(request):
  return HttpResponse("Hello World")


def messages(request):
  if request.method == "GET":
    messages = list(Message.objects.all().values())
    return HttpResponse(json.dumps(messages, cls=DateEncoder), content_type="application/json")

  if request.method == "POST":
    message = Message(
      recipient=get_object_or_404(User, name=request.POST['recipient']),
      sender=get_object_or_404(User, id=request.POST['sender']),
      body=request.POST['body']
    )
    message.save()

    return HttpResponseRedirect(reverse('chat:messages'))




def message_by_id(request, message_id):
  message = get_object_or_404(Message, id=message_id)
  return render(request, "chat/message.html", {'message': message})


def message_form(request, user_id):
  user = get_object_or_404(User, id=user_id)
  return render(request, "chat/send.html", {'user': user})

