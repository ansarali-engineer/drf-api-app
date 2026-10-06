from rest_framework import viewsets

from user.authentication import CustomJWTAuthentication, CustomTokenAuthentication
from .models import Customer
from rest_framework.authentication import BaseAuthentication, BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializer import CustomerSerializer
from user.permissions import HasRolePermission



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        CustomTokenAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated,HasRolePermission]
    throttle_classes = [UserRateThrottle]
    permission_screen = "customers"
    filter_backend = [DjangoFilterBackend,SearchFilter,OrderingFilter]
        
    filterset_fields = ['branch','assigned_to']

    search_fields = ['name','email','phone','company',]

    ordering_fields = ['created_at','name',]
