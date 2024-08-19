from django.contrib import admin
from .models import Agora, Stoa, AgoraStudy, AgoraOrator, StoaStudy, StoaMessage, AgoraStudyRequest

# Register your models here.
admin.site.register(Agora)
admin.site.register(Stoa)
admin.site.register(AgoraStudy)
admin.site.register(AgoraOrator)
admin.site.register(StoaStudy)
admin.site.register(StoaMessage)
admin.site.register(AgoraStudyRequest)