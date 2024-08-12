import base64
from hashlib import sha256

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from core.Utilities.permissions import IsAuthenticated
from core.models import Credential
from core.serializers import CredentialSerializer
from core.signals import credential_accessed

# Generate a key for encryption
key = base64.urlsafe_b64encode(sha256(settings.SECRET_KEY.encode()).digest())
cipher_suite = Fernet(key)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('service', openapi.IN_QUERY, description="Service name to filter credentials",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('tag', openapi.IN_QUERY, description="Tag name to filter credentials",
                          type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response('Successful retrieval of credentials', CredentialSerializer(many=True)),
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Credentials']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def list_credentials(request):
    service = request.query_params.get('service', None)
    tag = request.query_params.get('tag', None)
    filter_params = {}
    if service:
        filter_params['service__name__contains'] = service
    if tag:
        filter_params['tags__name__contains'] = tag

    if filter_params:
        credentials = Credential.objects.filter(**filter_params).select_related('service', 'created_by')
    else:
        credentials = Credential.objects.all().select_related('service', 'created_by')

    if not request.user.is_staff:
        credentials = credentials.filter(created_by=request.user) | credentials.filter(allowed_users=request.user)

    for credential in credentials:
        credential_accessed.send(sender=Credential, user=request.user, credential=credential)

    serializer = CredentialSerializer(credentials, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=CredentialSerializer,
    responses={
        201: openapi.Response('Credential created successfully', CredentialSerializer),
        400: 'Bad Request',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Credentials']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def create_credential(request):
    serializer = CredentialSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']
        serializer.save(created_by=request.user, password=password)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=CredentialSerializer,
    responses={
        200: openapi.Response('Credential updated successfully', CredentialSerializer),
        400: 'Bad Request',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Credentials']
)
@swagger_auto_schema(
    method='patch',
    request_body=CredentialSerializer,
    responses={
        200: openapi.Response('Credential updated successfully', CredentialSerializer),
        400: 'Bad Request',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Credentials']
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def update_credential(request, pk):
    try:
        credential = Credential.objects.get(pk=pk)
    except Credential.DoesNotExist:
        return Response("Credential not found", status=status.HTTP_404_NOT_FOUND)

    if (not request.user.is_staff and credential.created_by != request.user
            and request.user not in credential.allowed_users.all()):
        return Response("You do not have permission to update this credential", status=status.HTTP_403_FORBIDDEN)

    serializer = CredentialSerializer(credential, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to grant access')
        }
    ),
    responses={
        200: 'Access granted successfully',
        400: 'Bad Request',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Credentials']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def grant_access(request, pk):
    try:
        credential = Credential.objects.get(pk=pk)
    except Credential.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    credential.allowed_users.add(user)
    credential.save()
    return Response("Access granted successfully", status=status.HTTP_200_OK)
