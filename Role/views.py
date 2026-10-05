from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from user.authentication import CustomJWTAuthentication, CustomTokenAuthentication
from .models import Role,RolePermission
from .serializer import RoleSerializer,RolePermissionsSerializer

class RoleViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        CustomTokenAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RolePermissionsViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication,CustomTokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionsSerializer
