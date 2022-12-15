from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages', views.messages, name="messages"),
    path('chat', views.chat, name="chat"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
]
