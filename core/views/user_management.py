from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView

from core.serializers import UserSerializer


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
