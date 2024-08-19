from django.contrib import admin
from .models import UserMessage, UserConversation

# Register your models here.
admin.site.register(UserMessage)
admin.site.register(UserConversation)
