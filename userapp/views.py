from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
import re

PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

@api_view(['POST'])
# @permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    name = request.data.get('name')
    password = request.data.get('password')

    if email and name and password:
        if not re.match(PASSWORD_REGEX, password):
            return Response({'message': 'Invalid password. Password must be at least 8 characters long and contain at least one letter and one digit.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists. Please use a different email address.'}, status=status.HTTP_400_BAD_REQUEST)


        CustomUser.objects.create_user(email=email, name=name, password=password)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
