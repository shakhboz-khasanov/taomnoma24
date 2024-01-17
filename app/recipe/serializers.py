"""Recipe serializers"""

from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingridient,
)


class IngridientSerializer(serializers.ModelSerializer):
    """serializer class for ingridient objects"""

    class Meta:
        model = Ingridient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """serializer class for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer class for recipe objects"""
    tags = TagSerializer(many=True, required=False)
    ingridients = IngridientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes',
                  'price', 'link', 'tags', 'ingridients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """create a new recipe"""
        tags = validated_data.pop('tags', [])
        ingridients = validated_data.pop('ingridients', [])
        recipe = Recipe.objects.create(**validated_data)
        author = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=author,
                **tag,
            )
            recipe.tags.add(tag_obj)
        for ingridient in ingridients:
            ingridient_obj, created = Ingridient.objects.get_or_create(
                user=author,
                **ingridient,
            )
            recipe.ingridients.add(ingridient_obj)
        return recipe

    def update(self, instance, validated_data):
        """update a recipe"""
        tags = validated_data.pop('tags', [])
        ingridients = validated_data.pop('ingridients', [])
        recipe = super().update(instance, validated_data)
        author = self.context['request'].user
        if author != recipe.user:
            raise serializers.ValidationError(
                'You are not the author of this recipe.'
            )
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=author,
                **tag,
            )
            recipe.tags.add(tag_obj)
        for ingridient in ingridients:
            ingridient_obj, created = Ingridient.objects.get_or_create(
                user=author,
                **ingridient,
            )
            recipe.ingridients.add(ingridient_obj)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """serializer class for recipe detail objects"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
