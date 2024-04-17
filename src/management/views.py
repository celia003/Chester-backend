from django.conf import settings
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import F

from .models import User, Role, RoleUser

from .serializers import UsersListSerializer, UserSerializer, UserStatusSerializer, UsersSerializerCreate, RoleSerializer
from . import filters as filter_object

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, APIException, ValidationError

import logging



def index(request):
    return render(request, 'index.html', locals())


class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('-is_active', '-created')
    serializer_class = UsersListSerializer
    filterset_class = filter_object.UsersFilter

    def get_queryset(self):
        queryset = self.queryset

        return queryset.annotate(
            role_user=F('roleuser_user'),
            role_name=F('roleuser_user__role__name'),
            role_id=F('roleuser_user__role__id')
        )


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('-is_active', '-created')
    serializer_class = UserSerializer
    lookup_field = 'pk'
    pagination_class = None


class UserUpdateStatus(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    lookup_field = 'pk'

class UserUpdate(generics.RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated, utils.allowStaff, utils.checkRoles]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UsersSerializerCreate
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response=super().update(request, *args, **kwargs)

        # partial = kwargs.pop('partial', False)
        instance = self.get_object()

        try:
            ru, created = RoleUser.objects.get_or_create(user=instance)

            ru.user_id=instance.id
            ru.role_id=request.data['role_id']
            ru.save()
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        finally:
            return response


class UserCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UsersSerializerCreate


class RolesList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all().order_by('order')
    serializer_class = RoleSerializer
    pagination_class = None
