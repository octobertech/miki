from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from main.models import Link
from django.contrib.auth.models import User
from api.serializers import LinkSerializer, UserSerializer
from api.permissions import IsOwnerOrReadOnly



class MikiMixin(object):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.user_id = request.user


class MikiList(MikiMixin, ListCreateAPIView):
    pass


class MikiDetail(MikiMixin, RetrieveUpdateDestroyAPIView):
    pass


class UserMixin(object):
    id=None
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class UserList(UserMixin, ListCreateAPIView):
    pass


class UserDetail(UserMixin, RetrieveUpdateDestroyAPIView):
    pass


class UserMikiList(ListCreateAPIView):
    id=None
    queryset = Link.objects.filter(user_id=id)
    serializer_class = LinkSerializer
    permission_classes = (IsOwnerOrReadOnly,)



