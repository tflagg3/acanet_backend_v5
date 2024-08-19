from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import UserMessage, UserConversation
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def new_conversation(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        user2 = User.objects.filter(id=data['other_user']).first()
        conversation = UserConversation.objects.create(user1 = user, user2 = user2)
        conversation.save()
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def get_conversation(request):
    user = request.user
    data = request.data
    conversation = UserConversation.objects.filter(id = data['conversation_id'])
    if user == conversation[0].user1:
        other_user = conversation[0].user2.username
    elif user == conversation[0].user2:
        other_user = conversation[0].user1.username
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    print(conversation)
    messages = UserMessage.objects.filter(conversation = data["conversation_id"])
    serialized = []
    for message in messages:
        date_time = str(message.date).split(' ')
        # sent_by_this_user = (user == message.from_user)
        serialized.append({'id': str(message.id),
                           'content': message.message,
                           'sender': str(message.from_user.id),
                           'date': date_time.pop(0),
                           'time': date_time.pop(0).split('.')[0],
                           'currentUserId': str(user.id)})

    print(serialized)
    return Response({"message_list": serialized})


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def sendMessage(request):
    user = request.user
    conversation = UserConversation.objects.filter(id = request.data['conversation_id'])
    if user != conversation[0].user1 and user != conversation[0].user2:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    request_data = request.data
    request_data['from_user'] = user
    message = UserMessage.objects.create(**request_data)
    message.save()
    return Response(status=status.HTTP_200_OK)
    # create message in the database
    # add notification for the receiver?


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def getMyConversations(request):
    # we want the username, profile picture, most recent message and its date
    user = request.user
    conversations = UserConversation.objects.filter(user1 = user) | UserConversation.objects.filter(user2 = user)
    serialized = []
    for conversation in conversations:
        if conversation.user1 == user:
            other_user = conversation.user2
        else:
            other_user = conversation.user1

        messages = UserMessage.objects.filter(conversation=conversation)
        mrm = messages[len(messages) - 1]
        output = {'name': other_user.username}
        # try:
        #     output['profile_picture'] = other_user.userprofile.profile_picture
        # except ValueError as e:
        #     output['profile_picture'] = other_user.username[0]
        output['id'] = conversation.id
        if mrm is not None:
            output['message_content'] = mrm.message
            # print(mrm.date)
            date_time = str(mrm.date).split(' ')
            output['message_date'] = date_time.pop(0)
            output['message_time'] = date_time.pop(0).split('.')[0]
        serialized.append(output)

    return Response({'conversations': serialized})