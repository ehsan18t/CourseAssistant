from django.db import models
from base.models import User

# Models for the chat app
class PrivateChat(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    last_message = models.CharField(max_length=1000, blank=True, null=True)
    last_message_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user1} and {self.user2}'

class GroupChat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    last_message = models.CharField(max_length=1000, blank=True, null=True)
    last_message_time = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'

# If private chat, 'chat' and 'receiver' field will be filled and 'group' field will be null
# If group chat, 'group' field will be filled and 'chat' and 'receiver' field will be null
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender} : {self.message}'


