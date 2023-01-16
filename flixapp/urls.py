from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from pydantic import SecretStr
from django.contrib.auth.hashers import check_password
from user.models import User
from datetime import timedelta
import jwt
from jwt import encode, PyJWTError, decode
from django.shortcuts import get_object_or_404
from django.conf import settings


class TokenPayload(Schema):
    user_id: int=None

class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> User:
        user = self.get_current_user(token)
        if user:
            return user

    @staticmethod
    def get_current_user(token: str) -> User | None:
        """Check auth user"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            token_data = TokenPayload(**payload)
        except PyJWTError:
            return None
        user = get_object_or_404(User, email=payload['sub'])
        return user


api = NinjaAPI(
    auth=AuthBearer(),
    title='FlixFix',
    version="0.1.0",
)


class UserSchema(Schema):
    email:str
    password:str

class LoginSchema(Schema):
    email:str
    password:SecretStr

class AccessToken:
    @staticmethod
    def create(user: User) -> dict:
        email = user.email
        access_token_expires = timedelta(minutes=999999)
        token = AccessToken.create_secure_token(
            data={"sub": email},
            expires_delta=access_token_expires,
        )
        user.save()
        return {
            "email": email,
            "access_token": token,
        }


@api.post('/create-user', auth=None)
def create_user_api(request, payload:UserSchema):
    """Create User"""
    user = User.objects.create_user(
        payload.email,
        payload.password,
    )
    return {"id": user.id}   

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
