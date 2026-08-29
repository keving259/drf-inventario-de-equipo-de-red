from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({'error' : 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token" : token.key, "user" : serializer.data}, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'home.html')