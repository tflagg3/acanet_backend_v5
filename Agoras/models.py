from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import uuid as uuid_lib


# Create your models here.
class Agora(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    name = models.CharField(max_length=100)
    great_sophist = models.ForeignKey(User, on_delete=models.RESTRICT)
    private = models.BooleanField(default=False)
    bio = models.TextField()
    date_created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


class Stoa(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    agora = models.ForeignKey(Agora, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    stoa_sophist = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.agora.name + ' - ' + self.name


class AgoraOrator(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    agora = models.ForeignKey(Agora, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    promoted_on = models.DateTimeField(default=datetime.now())

class AgoraStudyRequest(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    agora = models.ForeignKey(Agora, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='agora_invite_from_user')
    requested_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username + ' - ' + self.agora.name

class AgoraStudy(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    agora = models.ForeignKey(Agora, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " in " + self.agora.name


class StoaStudy(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    channel = models.ForeignKey(Stoa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " in " + self.channel.name


class StoaMessage(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    channel = models.ForeignKey(Stoa, on_delete=models.CASCADE)
    message_content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + ': "' + self.message_content[:50] + '...'""

class StoaMessageReply(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    message = models.ForeignKey(StoaMessage, on_delete=models.CASCADE)
    message_content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.RESTRICT)


class MessageLike(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    message = models.ForeignKey(StoaMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MessageReplyLike(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
                          )
    message = models.ForeignKey(StoaMessageReply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



# we want a function to add a main channel to every group
# function to add a user to membership of main channel once added to group
# function to add group membership of admin upon creation of group