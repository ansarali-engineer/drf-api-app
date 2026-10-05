from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from user.authentication import CustomJWTAuthentication, CustomTokenAuthentication
from .models import Lead
from .serializer import LeadSerializer

class LeadViewSet(viewsets.ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        CustomTokenAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Lead.objects.all().order_by('-id')
    serializer_class = LeadSerializer

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]

    filterset_fields =['status','priority']
    search_fields =['title','source']
    ordering_fields = ['status','priority']