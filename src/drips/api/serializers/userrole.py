from django.contrib.auth import get_user_model

from rest_framework import serializers
from unicef_security.models import BusinessArea


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, trim_whitespace=True)
    last_name = serializers.CharField(required=True, trim_whitespace=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser')

    def validate_email(self, value):
        if value != value.lower():
            raise serializers.ValidationError("The email should be lowercase")
        return value


class BusinessAreaSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = BusinessArea
        fields = ('code', 'name', 'long_name', 'region', 'country')
