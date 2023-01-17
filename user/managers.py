from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password):
        """
        Create and save a User with the given email and password.
        """

        email_pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+\
                            (\.[A-Z|a-z]{2,})+'
        password_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[!@#?\]]).{10,}$'

        if not email:
            raise ValueError(_('Enter email'))

        if not re.fullmatch(email_pattern, email):
            raise ValueError(_('Invalid email'))

        if not password:
            raise ValueError(_('Enter password'))

        if not re.fullmatch(password_pattern, password):
            raise ValueError(_('Password does not comply with requirements'))

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()

        return user
