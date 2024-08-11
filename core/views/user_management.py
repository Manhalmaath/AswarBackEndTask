from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.Utilities.JWTAuth import create_token
from core.serializers import RegisterSerializer, LoginSerializer


@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={
        200: openapi.Response('Successful registration', RegisterSerializer),
        400: 'Bad Request',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Auth']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    payload = RegisterSerializer(data=request.data)

    if not payload.is_valid():
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    payload = payload.validated_data
    if payload['password1'] != payload['password2']:
        return Response({"detail": "Passwords does not match!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=payload['username'])
        return Response({"detail": "Forbidden, Username is already registered"}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        user = User.objects.create_user(first_name=payload['first_name'], last_name=payload['last_name'],
                                        username=payload['username'], email=payload['email'],
                                        password=payload['password1'])
        if user:
            return Response({"token": create_token(user.id)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "An error occurred, please try again."},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={
        200: openapi.Response('Successful login', LoginSerializer),
        400: 'Bad Request',
        401: 'Unauthorized'
    },
    tags=['Auth']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    payload = LoginSerializer(data=request.data)
    if not payload.is_valid():
        return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)

    payload = payload.validated_data

    user = authenticate(request, username=payload['username'], password=payload['password'])

    if user is not None:
        return Response({
            "token": create_token(user.id)}, status=status.HTTP_200_OK)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
