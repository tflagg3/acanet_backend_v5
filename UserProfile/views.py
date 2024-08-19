from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from .models import Follow

# Create your views here.
# everybody that this user is following
@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes((IsAuthenticated, ))
def get_following(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        follower_follows = Follow.objects.filter(follower=data['user'])
        out_data = []
        for follow in follower_follows:
            out_data.append({
                'id': follow.id,
                'user': follow.follower.username,
            })

        return Response(data={"following": out_data}, status=status.HTTP_200_OK)


def get_followers(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        followed_follows = Follow.objects.filter(followed=data['user'])
        out_data = []
        for follow in followed_follows:
            data.append({
                'id': follow.id,
                'user': follow.follower.username,
            })
        return Response(data={"followers": data}, status=status.HTTP_200_OK)