from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
)
from user.authentication import CustomJWTAuthentication, CustomTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializer import LeadActivitySerializer
from .models import LeadActivity


class LeadActivityViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        CustomTokenAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = LeadActivity.objects.all()
    serializer_class = LeadActivitySerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'lead',
        'user',
        'activity_type',
    ]

    search_fields = [
        'subject',
        'description',
        'activity_type',
    ]

    ordering_fields = [
        'activity_date',
        'created_at',
        'updated_at',
        'subject',
    ]