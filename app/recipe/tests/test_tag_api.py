"""Test cases for tag API endpoints."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')
RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(tag_id):
    """create and return tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(email="test@example.com", password="testpass123"):
    """Helper function for creating a user."""
    return get_user_model().objects.create_user(email, password)


def create_tag(user, name="Main course"):
    """Helper function for creating a tag."""
    return Tag.objects.create(user=user, name=name)


class PublicTagsApiTests(TestCase):
    """ Test the publicly available tags API. """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving tags. """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test the authorized user tags API. """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieving tags. """
        create_tag(user=self.user, name="Vegan")
        create_tag(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-id")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user. """
        user2 = create_user(email="user2@example.com", password="testpass321")
        create_tag(user=user2, name="Fruity")
        tag = create_tag(user=self.user, name="Comfort food")

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)
        self.assertEqual(response.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = create_tag(user=self.user)

        payload = {"name": "Updated tag name"}

        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        tag.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag(self):
        """Test deleting tag"""
        tag = create_tag(user=self.user)

        url = detail_url(tag.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertTrue(tags.count, 0)

    def test_create_tag_successful(self):
        """Test creating a new tag."""
        payload = {"name": "Test tag"}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_recipe_with_new_tag(self):
        """Test creating a recipe with new tag."""
        payload = {
            "title": "Test recipe",
            "time_minutes": 10,
            "price": 500,
            "tags": [{"name": "Test tag"}, {"name": "Test tag2"}],
        }
        response = self.client.post(RECIPE_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        for tag in recipe.tags.all():
            self.assertIn(tag.name, ["Test tag", "Test tag2"])

    def test_update_recipe_with_new_tag(self):
        """Test updating a recipe with new tag."""
        tag = create_tag(user=self.user, name="Test tag")
        recipe = Recipe.objects.create(
            user=self.user,
            title="Test recipe",
            time_minutes=10,
            price=500,
        )
        payload = {
            "title": "Test recipe",
            "time_minutes": 10,
            "price": 500,
            "tags": [{"name": "Test tag"}, {"name": "Test tag2"}],
        }
        url = detail_url(recipe.id)
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        for tag in recipe.tags.all():
            self.assertIn(tag.name, ["Test tag", "Test tag2"])
