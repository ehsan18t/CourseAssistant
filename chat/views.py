from django.contrib.auth.decorators import login_required
from .models import *
from base.models import User
from django.shortcuts import render, redirect

# Create your views here.
def get_chat_list_data(user):
    # Private chat
    user_list = Message.get_connected_users(user.id)
    message = []
    for u in user_list:
        m = Message.get_last_message(user.id, u.id)
        message.append(m)
    private = zip(user_list, message)

    # group chat
    chat_list = Study_Group.get_chats(user.id)
    message = []
    counts = []
    for c in chat_list:
        message.append(Study_Group.get_last_message(c.id))
        counts.append(Study_Group.get_unread_count(c.id, user.id))
    chat = zip(chat_list, message, counts)

    return chat, private


@login_required(login_url='login')
def chat_list(request):
    user = request.user  # get your primary key
    chat, private = get_chat_list_data(user)
    return render(request, 'chat/chat_list.html', {'chat':  chat, 'private': private})

@login_required(login_url='login')
def private_chat(request, pk):
    user = request.user
    user2 = User.objects.get(id = pk)
    o = Ditch.objects.filter(u1_id=user.id,u2_id=user2.id)
    
    
    if not o:
        ditched = 'Block'
        Ditch.objects.create(u1=user,u2=user2,ditched=False)
    elif o[0].ditched == False:
        ditched = 'Block'
    else :
        ditched = 'Unblock'


    if request.method == 'POST':
        d = request.POST.get('click')
        if d == 'Block':
            ditched = 'Unblock'
            if not o:
                Ditch.objects.create(u1=user,u2=user2,ditched=True)
            else :
                o[0].ditched = True
                o[0].save()
        elif d == 'Unblock' :
            o[0].ditched = False
            ditched = 'Block'
            o[0].save()
        else : 
            msg = request.POST['message']
            Message.objects.create(sender=user, recipient=user2, message=msg)
            return redirect('private_chat', pk=pk)
    
    # Private chat
    messages = Message.get_all_messages(user.id, user2.id)
    chat, private = get_chat_list_data(user)
    
    return render(request, 'chat/con_private.html', 
    {'messages' : messages,
        'other_user' : user2,
        'you' : user,
        'ditch' : ditched,
        'chat':  chat,
        'private': private
    })

@login_required(login_url='login')
def group_chat(request, pk):
    user = request.user

    if request.method == 'POST':
        send_message_gc(request, user, pk)
        return redirect('group_chat', pk=pk)

    group = Study_Group.objects.get(id=pk)
    chat, private = get_chat_list_data(user)

    # group chat
    g_msg = Study_Group.get_all_messages(pk, user)
    return render(request, 'chat/conversation.html', {'messages': g_msg, 'group': group, 'chat':  chat, 'private': private, 'me': user})

def send_message_gc(request, user, pk):
    msg = request.POST['message']
    study_group = Study_Group.objects.get(id=pk)
    m = Group_Message.objects.create(sender=user, study_group=study_group, message=msg)
    rr = Read_Report.objects.create(user=user, message=m)
    m.save()
    rr.save()
