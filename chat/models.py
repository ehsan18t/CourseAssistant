from django.db import models
from base.models import User


# Models for the chat app

# If private chat, 'chat' and 'receiver' field will be filled and 'group' field will be null
# If group chat, 'group' field will be filled and 'chat' and 'receiver' field will be null
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    # function gets all messages between 'the' two users (requires your pk and the other user pk)
    def get_all_messages(id_1, id_2):
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date') # get messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date') # get messages from recipient to sender
        for x in range(len(message2)):
            messages.append(message2[x])

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

    # function gets all messages between 'any' two users (requires your pk)
    def get_message_list(u):
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Message.objects.all():
            for_you = message.recipient == u  # messages received by the user
            from_you = message.sender == u  # messages sent by the user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    study_group = models.ForeignKey('Study_Group', on_delete=models.CASCADE, related_name='study_group')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'chat_participants'
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ('-date_joined',)

    # function gets all participants in a chat (requires chat pk)
    @staticmethod
    def get_participants(id):
        return Participant.objects.filter(study_group=id)

    # function gets all chats a user is in (requires user pk)
    @staticmethod
    def get_chats(id):
        return Participant.objects.filter(user=id)

class Study_Group(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_study_groups'
        verbose_name = 'Study Group'
        verbose_name_plural = 'Study Groups'
        ordering = ('-date_created',)

class Group_Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    study_group = models.ForeignKey(Study_Group, on_delete=models.CASCADE, related_name='study_group')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_group_messages'
        verbose_name = 'Group Message'
        verbose_name_plural = 'Group Messages'
        ordering = ('-date',)

    # function gets all messages in a chat (requires chat pk)
    @staticmethod
    def get_all_messages(id):
        # get messages in the chat, sort them by date(reverse) and add them to the list
        messages = Group_Message.objects.filter(study_group=id).order_by('-date')

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            if messages[x].is_read == False:
                messages[x].is_read = True
                messages[x].save()
        
        return messages
