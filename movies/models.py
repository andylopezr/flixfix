from django.db import models
from django.conf import settings
# import uuid
# import os


# def poster_file_path(instance, filename):
#     """Generate file path for movie poster."""
#     ext = os.path.splitext(filename)[1]
#     filename = f'{uuid.uuid4()}{ext}'

#     return os.path.join('uploads', 'recipe', filename)


class Movie(models.Model):
    """Movie object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField(blank=True)
    review = models.TextField(blank=True)
    is_private = models.BooleanField(default=True)
    # poster = models.ImageField(null=True, upload_to=poster_file_path)

    def __str__(self):
        return self.title
