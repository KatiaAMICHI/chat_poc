from django.urls import path
from .views import send_message, get_user_messages

urlpatterns = [
    path('send-message/', send_message, name='send_message'),
    path('get_user_messages/', get_user_messages, name='get_user_messages'),
]
