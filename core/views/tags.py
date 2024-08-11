from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from core.Utilities.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Tag
from core.serializers import TagSerializer

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of tags', TagSerializer(many=True)),
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Tags']
)
@swagger_auto_schema(
    method='post',
    request_body=TagSerializer,
    responses={
        201: openapi.Response('Tag created successfully', TagSerializer),
        400: 'Bad Request',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Tags']
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tag_list_create(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of tag', TagSerializer),
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Tags']
)
@swagger_auto_schema(
    method='put',
    request_body=TagSerializer,
    responses={
        200: openapi.Response('Tag updated successfully', TagSerializer),
        400: 'Bad Request',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Tags']
)
@swagger_auto_schema(
    method='delete',
    responses={
        204: 'Tag deleted successfully',
        404: 'Not Found',
        403: 'Forbidden',
        500: 'Internal Server Error'
    },
    tags=['Tags']
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def tag_detail(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)