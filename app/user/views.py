"""
Views for the user app API.
"""

from rest_framework import generics

# local imports
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    """
    serializer_class = UserSerializer
