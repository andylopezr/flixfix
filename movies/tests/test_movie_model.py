from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from movies.models import Movie

def create_user(email='user@example.com', password='Testpassword!'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)

class MovieTests(TestCase):
    """Test models."""

    def test_create_movie(self):
            """Test creating a movie is successful."""
            user = get_user_model().objects.create_user(
                'test@example.com',
                'Testpassword!',
            )
            movie = Movie.objects.create(
                user=user,
                title='Avatar',
                score=Decimal('8.3'),
                description='Sample movie description.',
                review='Sample review...'
            )

            self.assertEqual(str(movie), movie.title)