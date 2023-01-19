from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from pydantic import SecretStr
from django.contrib.auth.hashers import check_password
from user.models import User
from movies.models import Movie
from datetime import timedelta, datetime
from jwt import encode, PyJWTError, decode
from django.shortcuts import get_object_or_404
from django.conf import settings
from ninja.pagination import paginate
from typing import List
from django.db.utils import IntegrityError
import requests


class TokenPayload(Schema):
    user_id: int = None


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> User:
        user = self.get_current_user(token)
        if user:
            return user

    @staticmethod
    def get_current_user(token: str) -> User | None:
        """Check auth user"""
        try:
            payload = decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])

        except PyJWTError:
            return None
        user = get_object_or_404(User, email=payload['sub'])
        return user


api = NinjaAPI(
    auth=AuthBearer(),
    title='FlixFix',
    version="0.1.0",
)

# Django Ninja schemas ------------------------------------------------------


class UserSchema(Schema):
    email: str
    password: str


class getUserSchema(Schema):
    id: int
    email: str


class LoginSchema(Schema):
    email: str
    password: SecretStr


class MovieSchema(Schema):
    title: str
    score: float
    description: str
    review: str
    is_private: bool


class getMovieSchema(Schema):
    id: int
    title: str
    score: float
    description: str
    review: str
    is_private: bool


class editMovieSchema(Schema):
    title: str
    score: float
    description: str
    review: str
    is_private: bool


# Django Ninja AccessToken --------------------------------------------------

class AccessToken:
    @staticmethod
    def create(user: User) -> dict:
        email = user.email
        access_token_expires = timedelta(minutes=999999)
        token = AccessToken.create_token(
            data={"sub": email},
            expires_delta=access_token_expires,
        )
        user.save()
        return {
            "email": email,
            "access_token": token,
        }

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm="HS256"
        )
        return encoded_jwt


# User routes ---------------------------------------------------------------

# User creation
@api.post('/create-user', auth=None)
def create_user_api(request, payload: UserSchema):
    """
        Create a new user using email and password.

        Password constrains:

            - At least 10 characters long.

            - Should include one lowercase letter.

            - Should include one UPPERCASE letter.

            - Should include one of these special characters: ! @ # ? ]

    """
    try:
        user = User.objects.create_user(
            payload.email,
            payload.password,
        )

    except IntegrityError:
        return api.create_response(
            request,
            {"error": "Email already exists"},
            status=409,
        )

    return {
        "id": user.id,
        "email": user.email,
        }


# Login
@api.post('/login', auth=None)
def user_login(request, payload: LoginSchema):
    """Login using email and password"""
    try:
        user = User.objects.get(email=payload.email)

    except Exception:
        return api.create_response(
            request,
            {"error": "User not found"},
            status=404)

    if check_password(payload.password.get_secret_value(), user.password):
        return AccessToken.create(user)


# List all users
@api.get('/users', response=List[getUserSchema], auth=None)
@paginate
def get_users(request):
    """Lists all users"""
    all_users = User.objects.all()
    return all_users


# List user by id
@api.get('/users/{user_id}', response=getUserSchema, auth=None)
def get_user(request, user_id: int):
    """List a single user by id"""
    user = get_object_or_404(User, id=user_id)
    return user


# TODO: Fix bug where update does not meet the user creation requirements
# Update User
@api.put('/users/{user_id}', auth=None)
def update_user(request, user_id: int, payload: UserSchema):
    """Update user attributes"""
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return api.create_response(
            request,
            {"message": "Updated successfully"},
            status=204)


# Delete user
@api.delete('/users/{user_id}', auth=None)
def delete_user(request, user_id: int):
    """Delete a user by id"""
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return api.create_response(
            request,
            {"message": "Deleted successfully"},
            status=204)


# Movie routes --------------------------------------------------------------

# Creates a Movie post
@api.post('/movie')
def create_movie(request, payload: MovieSchema):
    """Add a new movie"""
    movie_form = {
        'user': request.auth,
        'title': payload.title,
        'score': payload.score,
        'description': payload.description,
        'review': payload.review,
        'is_private': payload.is_private,
    }
    movie = Movie.objects.create(**movie_form)
    return api.create_response(
            request,
            {"title": movie.title},
            status=201)


# List public Movie posts
@api.get('/list_all_movies', response=List[getMovieSchema], auth=None)
@paginate
def get_public_movies(request):
    """List all public movie posts"""
    public_movies = Movie.objects.filter(is_private=False)
    return public_movies


# List User Movie posts
@api.get('/list_user_movies', response=List[getMovieSchema])
@paginate
def get_user_movies(request, is_private: bool):
    """List all private or public movies created by user"""
    if is_private is True:
        movies = Movie.objects.filter(user=request.auth, is_private=True)
    else:
        movies = Movie.objects.filter(user=request.auth, is_private=False)

    return movies


# Update a Movie
@api.put('/movie/{movie_id}')
def update_movie(request, movie_id: int, payload: editMovieSchema):
    """Update a movie using id"""
    try:
        movie = Movie.objects.get(id=movie_id, user=request.auth)
        for attr, value in payload.dict().items():
            setattr(movie, attr, value)
        movie.save()
        return api.create_response(
            request,
            {"message": "Updated successfully"},
            status=204)

    except Exception:
        return api.create_response(
            request,
            {"error": "Unauthorized"},
            status=401)


# Delete a Movie
@api.delete('/movie/{movie_id}')
def delete_movie(request, movie_id: int):
    """Delete a movie using id"""
    try:
        movie = Movie.objects.get(id=movie_id, user=request.auth)
        movie.delete()
        return api.create_response(
            request,
            {"message": "Deleted successfully"},
            status=204)

    except Exception:
        return api.create_response(
            request,
            {"error": "Unauthorized"},
            status=401,)


# Random number ------------------------------------------------------------

@api.get('/number/', auth=None)
def random_number(request):
    """Gets random number from public API"""
    url = 'http://www.randomnumberapi.com/api/v1.0/randomnumber'
    r = requests.get(url)
    return {'number': r.text}


# Django routes ------------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
