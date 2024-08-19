from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Agora, Stoa, AgoraOrator, AgoraStudy, StoaStudy, StoaMessage, AgoraStudyRequest
from django.contrib.auth.models import User
# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def create_agora(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        agora = Agora.objects.create(name=data['name'],
                                     great_sophist=user,
                                     private=data['private'],
                                     bio=data['bio'])
        agora.save()
        main_stoa = Stoa.objects.create(agora=agora,
                                        name="main",
                                        stoa_sophist=user,
                                        private=data['private'])
        main_stoa.save()
        great_sophist_orator = AgoraOrator.objects.create(agora=agora,
                                                          user=user)
        great_sophist_orator.save()
        great_sophist_study = AgoraStudy.objects.create(agora=agora,
                                                        user=user)
        great_sophist_study.save()
        great_sophist_stoa_membership = StoaStudy.objects.create(channel=main_stoa,
                                                            user=user)
        great_sophist_stoa_membership.save()
        init_message = StoaMessage.objects.create(channel=main_stoa,
                                                  message_content="Welcome to the main stoa. Let's get to work",
                                                  sender=user)
        init_message.save()
        data['id'] = agora.id

        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_my_agoras(request):
    user = request.user
    my_agoras = AgoraStudy.objects.filter(user=user)
    agoras = [agora_membership.agora for agora_membership in my_agoras]
    serialized = []
    for agora in agoras:
        serialized.append({
            "id": agora.id,
            "name": agora.name,
            "bio": agora.bio,
            "isPrivate": agora.private,
        })
    print(serialized)
    return Response({'groups': serialized})

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_agora(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
        except Agora.DoesNotExist:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if agora.private:
            # make sure this user is a study of this agora
            try:
                study = AgoraStudy.objects.get(agora=agora, user=user)
            except AgoraStudy.DoesNotExist:
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={'name': agora.name, "id": agora.id, "bio": agora.bio}, status=status.HTTP_200_OK)
        else:
            return Response(data={'name': agora.name, "id": agora.id, "bio": agora.bio}, status=status.HTTP_200_OK)

    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_agora_stoae(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])

            agora_study = AgoraStudy.objects.get(agora=agora, user=user)
        except Agora.DoesNotExist:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except AgoraStudy.DoesNotExist:
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        stoae = Stoa.objects.filter(agora=agora)
        print(stoae)
        serialized = []
        for stoa in stoae:
            # this try block needs to be redone, don't want to except just to pass
            try:
                print(stoa.name)
                print(user)
                stoa_study = StoaStudy.objects.get(channel=stoa, user=user)
                serialized.append({'name': stoa.name, 'id': stoa.id})
            except StoaStudy.DoesNotExist:
                pass
        return Response(data={'stoae': serialized}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_stoa(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            stoa = Stoa.objects.get(id = data['stoa'])
            agora = stoa.agora
        except Stoa.DoesNotExist:
            return Response(data={'message': "stoa not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Agora.DoesNotExist:
            return Response(data={'message': "agora not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if stoa.private:
            try:
                stoa_study = StoaStudy.objects.get(channel=stoa,
                                                   user=user)
                agora_study = AgoraStudy.objects.get(agora=agora,
                                                     user=user)
            except StoaStudy.DoesNotExist:
                return Response(data={'message': "not study of this stoa"},
                                status=status.HTTP_401_UNAUTHORIZED)
            except AgoraStudy.DoesNotExist:
                return Response(data={'message': "not study of this agora"},
                                status=status.HTTP_401_UNAUTHORIZED)
            # need to get all the messages and send them back, along with the name?
            messages = StoaMessage.objects.filter(channel=stoa)
            messages_serialized = []
            for message in messages:
                date_time = str(message.date).split(' ')
                messages_serialized.append({'id': message.id,
                                            'sender_name': message.sender.username,
                                            'sender_id': message.sender.id,
                                            'content': message.message_content,
                                            'date': date_time.pop(0),
                                            'time': date_time.pop(0).split(".")[0],
                                            'currentUserId': user.id}
                                            )
            print(messages_serialized)
            return Response(data={'messages': messages_serialized}, status=status.HTTP_200_OK)
        # first make sure that

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def request_agora_study(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
            agora_study = AgoraStudy.objects.filter(agora=agora, user=user)
            if agora_study:
                return Response(data={'message': "This user is already a study of this agora"},
                                status=status.HTTP_400_BAD_REQUEST)

            if agora.private:
                agora_request = AgoraStudyRequest.objects.filter(agora=agora,
                                                                 from_user=user)
                if agora_request:
                    return Response(data={'message': "This has already sent a request to this agora"},
                                    status=status.HTTP_400_BAD_REQUEST)

                request = AgoraStudyRequest.objects.create(agora=agora,
                                                           from_user=user)
                request.save()
                # Notify the orators


                return Response({"message": "the request has been received"}, status=status.HTTP_201_CREATED)
            else:
                membership = AgoraStudy.objects.create(agora=agora, user=user)
                membership.save()
                return Response({"message": "you have succesfully joined " + agora.name}, status=status.HTTP_201_CREATED)
        except Agora.DoesNotExist:
            return Response({"message": "Agora not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def admit_agora_request(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora_request = AgoraStudyRequest.objects.get(id=data['request'])
            agora_orator = AgoraOrator.objects.get(agora=agora_request.agora, user=user)
            if data["admit"]:
                study = AgoraStudy.objects.create(agora=agora_request.agora,
                                              user=agora_request.from_user)
                study.save()
                agora_request.delete()
                # notify user that they have been accepted
                return Response(data={"message": "user has been admitted"}, status=status.HTTP_201_CREATED)
            else:
                agora_request.delete()
                # notify user that they have been denied
                return Response(data={"message": "agora request has been deleted"}, status=status.HTTP_200_OK)
        except Agora.DoesNotExist:
            return Response(data={'message': "Agora not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except AgoraOrator.DoesNotExist:
            return Response(data={'message': "Not authorized to admit requests"},
                            status=status.HTTP_401_UNAUTHORIZED,)
        except AgoraStudyRequest.DoesNotExist:
            return Response(data={'message': "Request not found"})

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_agora_study_requests(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
            user_orator = AgoraOrator.objects.get(agora=agora,
                                                  user=user)
            agora_requests = AgoraStudyRequest.objects.filter(agora=agora)
            requests = []
            for request in agora_requests:
                requests.append({'username': request.from_user.username,
                                 'id': request.id})

            return Response(data={'requests': requests}, status=status.HTTP_200_OK)
        except Agora.DoesNotExist:
            return Response(data={'message': "Agora not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except AgoraOrator.DoesNotExist:
            return Response(data={'message': "Not authorized to admit requests"},
                            status=status.HTTP_401_UNAUTHORIZED,)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def add_agora_orator(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
            orators = AgoraOrator.objects.filter(agora=agora)
            orators = [orator.user for orator in orators]
            if user not in orators:
                return Response(data=data,
                                status=status.HTTP_401_UNAUTHORIZED)
            other_user = User.objects.get(id=data['new_orator'])
            other_study = AgoraStudy.objects.filter(agora=agora, user=user)
            if not other_study:
                return Response(data={"message": "This user is not a study of this Agora"},
                                status=status.HTTP_400_BAD_REQUEST)
            other_orator = AgoraOrator.objects.filter(agora=agora, user=other_user)
            if other_orator:
                return Response(data={"message": "User is already an orator of the agora"}, status = status.HTTP_400_BAD_REQUEST)
            new_orator = AgoraOrator.objects.create(agora=agora,
                                                    user=other_user)
            new_orator.save()
            return Response(data={"message": "user has been promoted to orator"}, status=status.HTTP_201_CREATED)
        except Agora.DoesNotExist:
            return Response(data={'message': "agora not found"},
                            status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def demote_orator(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
            if agora.great_sophist == user:
                orator = User.objects.get(id=data['orator'])
                demotee = AgoraOrator.objects.get(agora=agora,
                                                  user=orator)
                demotee.delete()
                return Response(data={"message": "user has been demoted"}, status=status.HTTP_201_CREATED)
            else:
                return Response(data={"message": "You are not authorized to demote orator"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Agora.DoesNotExist:
            return Response(data={'message': "Agora not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except AgoraOrator.DoesNotExist:
            return Response(data={'message': "user is not an orator"},
                            status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def remove_study(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            agora = Agora.objects.get(id=data['agora'])
            userOrator = AgoraOrator.objects.get(agora=agora,
                                                 user=user)
            study = User.objects.get(id=data['study'])
            other_orator = AgoraOrator.objects.filter(agora=agora,
                                                      user=study)
            if other_orator:
                output = "You may not remove orators"
                if user == agora.great_sophist:
                    output = output + ". You must demote them first."
                return Response(data={"message": "You may not remove orators"},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response(data={"message": "user has been removed"},
                            status=status.HTTP_200_OK)
        except Agora.DoesNotExist:
            return Response(data={'message': "Agora not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except AgoraOrator.DoesNotExist:
            return Response(data={'message': "user is not an orator"},
                            status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def add_stoa(request):
    data = request.data
    user = request.user
    if user.is_authenticated:
        agora = Agora.objects.get(id=data['agora_id'])
        stoa = Stoa.objects.create(agora=agora,
                                   name=data['name'],
                                   stoa_sophist=user,
                                   private=data['private'])
        stoa.save()
        agora_great_sophist = StoaStudy.objects.create(channel=stoa,
                                                       user=agora.great_sophist)
        agora_great_sophist.save()
        stoa_sophist = StoaStudy.objects.create(channel=stoa,
                                                user=user)
        stoa_sophist.save()
        data['stoa_id'] = stoa.id
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def add_stoa_study(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        stoa_study = StoaStudy.objects.create(channel=data['channel'], user=data['user_id'])
        stoa_study.save()
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def send_stoa_message(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        try:
            stoa = Stoa.objects.get(id=data['stoa'])
            stoa_study = StoaStudy.objects.get(channel=stoa, user=user)
            new_message = StoaMessage.objects.create(channel=stoa,
                                                     message_content=data['content'],
                                                     sender=user)
            new_message.save()
            return Response({"messge": "message sent"}, status=status.HTTP_201_CREATED)
        except Stoa.DoesNotExist:
            return Response(data={'message': "Stoa not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except StoaStudy.DoesNotExist:
            return Response(data={'message': "not authorized for this stoa"},
                            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def send_message_reply(request):
    pass

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def like_message(request):
    pass

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def like_reply(request):
    pass
