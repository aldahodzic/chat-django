from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Message

# Create your views here.

def hello(request):
  return HttpResponse("Hello World")

def messages(request):
  if request.method == "GET":
    return render(
      request,
      'chat/messages.html', {
        "messages": Message.objects.all()
    })


def messageById(request, message_id):
  message = get_object_or_404(Message, id=message_id)
  return render(request, "chat/message.html", {'message': message})
