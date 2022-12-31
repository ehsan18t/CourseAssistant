from django.urls import path

from . import views
from chat.views import chat_list

urlpatterns = [
    path('', views.home, name="home"),
    path('content=<int:pk>', views.content_view, name="content_view"),
    path('content_approval', views.content_approval, name="content_approval"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('signup', views.signup, name="signup"),
    path('notification', views.notification_view, name="notification"),
    path('profile', views.user_profile, name="profile"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('profile=<int:pk>', views.others_profile, name="others_profile"),
]
