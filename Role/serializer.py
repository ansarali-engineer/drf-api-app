from rest_framework import serializers
from .models import Role,RolePermission


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields =['id','created_at','updated_at']

class RolePermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'
        read_only_fields =['id','created_at','updated_at']