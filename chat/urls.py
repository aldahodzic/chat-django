from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
  path('hello/', views.hello, name="hello"),
  path('messages/', views.messages, name="messages"),
  path('messages/<int:message_id>', views.message_by_id, name="message")
]
