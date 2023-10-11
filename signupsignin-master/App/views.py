from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser
from .serializers import UserSignInSerializer

###This handles user signup####

User = get_user_model()

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        web_terms = request.data.get('web_terms')
        dataprocessing = request.data.get('dataprocessing')
        subscription = request.data.get('subscription')

        if not any([username, email, phone_number]):
            return Response({'error': 'Please provide at least one of username, email, or phone_number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        
        existing_user_query = Q()
        
        if username:
         existing_user_query |= Q(email__iexact=username)
        if email:
            existing_user_query |= Q(email__iexact=email)
        if phone_number:
            existing_user_query |= Q(phone_number__iexact=phone_number)

        existing_user = CustomUser.objects.filter(existing_user_query).exists()

        if existing_user:
            return Response({'error': 'Username, email, or phone_number already exists'}, status=status.HTTP_409_CONFLICT)


        # Create a new user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            password=hashed_password,
            web_terms=web_terms,
            dataprocessing=dataprocessing,
            subscription=subscription
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
User = get_user_model()

# This view handles user sign in username,phone_number,email=="identifier"- & password  for signin
@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        identifier = request.data.get('identifier')
        password = request.data.get('password')
        
        if identifier is None or password is None:
            return Response({'error': 'Both identifier and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the type of identifier based on its format
        identifier_type = 'username'
        if '@' in identifier:
            if '.' in identifier.split('@')[1]:
                identifier_type = 'email'
        elif identifier.isdigit() and len(identifier) == 10:
            identifier_type = 'phone_number'

        user = None
        if identifier_type == 'username':
            user = CustomUser.objects.filter(username=identifier).first()
        elif identifier_type == 'email':
            user = CustomUser.objects.filter(email=identifier).first()
        elif identifier_type == 'phone_number':
            user = CustomUser.objects.filter(phone_number=identifier).first()

        if user and user.check_password(password):
            return Response({'message': 'Signin successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# This view handles user login and returns a token upon successful authentication
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# It seems you have a block of code here that might be out of place.
# This code block checks for an existing user, but it's not associated with any specific request method.
# Depending on your intention, you might need to move this code to an appropriate view or function.
    existing_user = CustomUser.objects.filter(
    Q(username__iexact=username) | Q(email__iexact=email) | Q(phone_number__iexact=phone_number)
     ).exists()

    if existing_user:
     return Response({'error': 'Username, email, or phone_number already exists'}, status=status.HTTP_409_CONFLICT)


















































