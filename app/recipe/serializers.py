"""Recipe serializers"""

from rest_framework import serializers
from core.models import (
    Recipe,
    Tag
)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer class for recipe objects"""

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """serializer class for recipe detail objects"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)


class TagSerializer(serializers.ModelSerializer):
    """serializer class for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
