from django.urls import path
from rest_framework.routers import DefaultRouter
from Role.views import RoleViewSet,RolePermissionsViewSet
router = DefaultRouter()
router.register('roles',RoleViewSet,basename='roles')
router.register('rolespermissions',RolePermissionsViewSet,basename='rolespermissions')
urlpatterns =[]
urlpatterns += router.urls