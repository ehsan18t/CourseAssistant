from django.http import JsonResponse
from django.contrib.auth import login
from .models import Message
from base.models import User
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'prMessages_list.html'
    login_url = 'login'

    # context data for latest message to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)  # get your primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)


        context['messages_list'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context

class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'prInbox.html'
    login_url = 'login'
    queryset = User.objects.all()


    # to send a message (pass the username instead of the primary key to the post function)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    # overide detailview default request pk or slug to get username instead
    def get_object(self):
        UserName= self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)



    # context data for the chat view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)  # get your primary key
        other_user = User.objects.get(username=self.kwargs.get("username"))  # get the other user's primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name from the message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        sender = other_user  # the sender of the message will be the recipient of the most recent message after it's sent
        recipient = user # the recipient of the message will be the sender of the most recent message after it's sent

        context['messages'] = Message.get_all_messages(sender, recipient)  # get all the messages between the sender(you) and the recipient (the other user)
        context['messages_list'] = messages # for MessagesListView template
        context['other_person'] = other_user  # get the other person you are chatting with from the username provided
        context['you'] = user  # send your primary key to the post
        context['other_users'] = other_users

        return context

    # send a message
    def post(self, request, *args, **kwargs):
        # print("sender: ", request.POST.get("you"))
        # print("recipient: ", request.POST.get('recipient'))
        sender = User.objects.get(pk=request.POST.get('you'))  # get the sender of the message(the person sending it)
        recipient = User.objects.get(pk=request.POST.get('recipient'))  # get the recipient of the message(You)
        message = request.POST.get('message')  # get the message from the form

        # if the sender is logged in, send the message
        if request.user.is_authenticated:
            if request.method == 'POST':
                if message:
                    Message.objects.create(sender=sender, recipient=recipient, message=message)
            return redirect('chat:inbox', username=recipient.username)  # redirect to the inbox of the recipient

        else:
            return render(request, 'login.html')

class UserListsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'prUsers_list.html'
    context_object_name = 'users'
    login_url = 'login'

    # context data for the users list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)  # get your primary key
        context['users'] = User.objects.exclude(pk=user.pk)  # get all the users except you
        return context
