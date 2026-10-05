from rest_framework import serializers
from .models import LeadActivity


class LeadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadActivity
        fields = '__all__'
        read_only_fields =['id','created_at','updated_at']