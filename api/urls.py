from django.urls import path
from . import views
from Agoras import views as agoras_views
from UserMessages import views as user_messages_views

urlpatterns = [
    path("conversations", user_messages_views.getMyConversations),
    path('new_conversation', user_messages_views.new_conversation),
    path("conversation", user_messages_views.get_conversation),
    path("sendMessage", user_messages_views.sendMessage),
    path('login', views.login),
    path('register', views.register),
    path('create_agora', agoras_views.create_agora),
    path('get_my_agoras', agoras_views.get_my_agoras),
    path('get_agora', agoras_views.get_agora),
    path('request_agora_study', agoras_views.request_agora_study),
    path('get_agora_study_requests', agoras_views.get_agora_study_requests),
    path('admit_agora_request', agoras_views.admit_agora_request),
    path('send_stoa_message', agoras_views.send_stoa_message),
    path('add_agora_orator', agoras_views.add_agora_orator),
    path('demote_orator', agoras_views.demote_orator),
    path('remove_study', agoras_views.remove_study),
    path('get_agora_stoae', agoras_views.get_agora_stoae),
    path('get_stoa', agoras_views.get_stoa),
    path('add_stoa', agoras_views.add_stoa),
    path('add_stoa_studyr', agoras_views.add_stoa_study),
]