from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid as uuid_lib
# Create your models here.

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid_lib.uuid4,
                          unique=True,
                          editable=False
    )
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower.username + ' follows ' + self.following.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)