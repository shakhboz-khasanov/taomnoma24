"""Test cases for tag API endpoints."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


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
