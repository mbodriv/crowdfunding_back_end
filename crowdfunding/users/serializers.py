from rest_framework import serializers
from .models import CustomUser

class CustomerUserSerializer (serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        field = '__all__'
        extra_kwargs = {'password': {'write only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)