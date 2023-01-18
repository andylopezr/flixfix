"""
Tests for recipe APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase

from movies.models import Movie

from rest_framework import status
from rest_framework.test import APIClient

from movie.serializers import MovieSerializer

MOVIES_URL = "http://127.0.0.1:8000/api/movie"
# TODO: check user creation url and response once it is live in AWS


def create_user(email='user@example.com', password='Testpassword!'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


def create_movie(user, **params):
    """Create and return a sample movie."""
    defaults = {
        'title': 'Avatar',
        'score': Decimal('8.3'),
        'description': 'Sample description',
        'review': 'Sample review',
    }
    defaults.update(params)

    movie = Movie.objects.create(user=user, **defaults)
    return movie


class PublicMovieAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(MOVIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='t@e.com', password='Testpassword!')
        self.client.force_authenticate(self.user)

    def test_retrieve_movies(self):
        """Test retrieving a list of movies."""
        create_movie(user=self.user)
        create_movie(user=self.user)

        res = self.client.get(MOVIES_URL)

        movies = Movie.objects.all().order_by('-id')
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_movie_list_limited_to_user(self):
        """Test list of movies is limited to authenticated user."""
        other_user = create_user(email='t@e.com', password='Testpassword!')
        create_movie(user=other_user)
        create_movie(user=self.user)

        res = self.client.get(MOVIES_URL)

        movies = Movie.objects.filter(user=self.user)
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
