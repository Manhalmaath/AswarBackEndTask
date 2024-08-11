from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from core.Utilities.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Service
from core.serializers import ServiceSerializer

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of services', ServiceSerializer(many=True)),
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Services']
)
@swagger_auto_schema(
    method='post',
    request_body=ServiceSerializer,
    responses={
        201: openapi.Response('Service created successfully', ServiceSerializer),
        400: 'Bad Request',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Services']
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def service_list_create(request):
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of service', ServiceSerializer),
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Services']
)
@swagger_auto_schema(
    method='put',
    request_body=ServiceSerializer,
    responses={
        200: openapi.Response('Service updated successfully', ServiceSerializer),
        400: 'Bad Request',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Services']
)
@swagger_auto_schema(
    method='delete',
    responses={
        204: 'Service deleted successfully',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Services']
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)