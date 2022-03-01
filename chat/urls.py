from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
  path('messages', views.Messages.as_view(), name="messages"),
  path('messages/<int:message_id>', views.MessageById.as_view(), name="message"),
  path('users', views.Users.as_view(), name="users"),
  path('users/<int:user_id>', views.UserById.as_view(), name="user"),
  path('send/<int:user_id>', views.message_form, name="message_form")
]
