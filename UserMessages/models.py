from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid as uuid_lib

class UserConversation(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    def __str__(self):
        return self.user1.username + ' and ' + self.user2.username

class UserMessage(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    conversation = models.ForeignKey(UserConversation, on_delete=models.CASCADE, related_name='conversation')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        if len(self.message) > 40:
            return self.message[:40]
        else:
            return self.message

def first_message(sender, instance, created, **kwargs):
    if created:
        initial_message = UserMessage(conversation=instance, from_user = instance.user1, date = datetime.now(), message = "Say Hi")
        initial_message.save()


post_save.connect(first_message, sender=UserConversation)