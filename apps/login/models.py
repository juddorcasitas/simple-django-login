from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model


class User(AbstractUser):
    date_joined = models.DateTimeField('date_joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    email_verified = models.BooleanField('email_verified', default=False)

    class Meta(object):
        unique_together = ('email',)
