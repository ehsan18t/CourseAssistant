from django.db import models
from base.models import User


# Models for the private chat and the group chat
class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    messages = models.ManyToManyField('Message', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user1) + ' - ' + str(self.user2)


class GroupChat(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    messages = models.ManyToManyField('Message', blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender) + ' - ' + str(self.timestamp)


