from django.urls import path

from .views import InboxView, UserListsView, MessagesListView

urlpatterns = [
    path('', MessagesListView.as_view(), name='message_list'),
    path('meet/', UserListsView.as_view(), name='users_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
]