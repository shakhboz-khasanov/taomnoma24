"""
Serializers for user app API views
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        """Meta class for user serializer"""

        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
