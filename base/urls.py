from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages', views.messages_page, name="messages"),
    # path('chat', views.chat, name="chat"),
    path('content_approval', views.content_approval, name="content_approval"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('signup', views.signup, name="signup"),
]
