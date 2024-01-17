"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='test@example.com', password='testpass123'):
    """
    Helper function for creating a user.
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """
    Test cases for models.
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized.
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='testpass123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_new_superuser(self):
        """
        Test creating a new superuser.
        """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test for creating a recipe"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=1_000_000,
            description='Test Recipe Description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test for creating a tag successfully"""
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Test Tag1'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredien(self):
        """Test for creating an ingredient successfully"""
        user = create_user()
        ingredient = models.Ingridient.objects.create(
            user=user,
            name='Test Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)
