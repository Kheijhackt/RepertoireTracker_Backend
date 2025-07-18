from rest_framework import serializers
from .models import AppUser

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'display_name', 'password', 'repertoire', 'created_at']
        read_only_fields = ['created_at', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
            'token': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AppUser(**validated_data)
        user.set_password(password)
        user.generate_token()
        user.save()
        return user
