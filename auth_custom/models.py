from django.contrib.auth.models import AbstractUser
from django.db import models


# custom the default user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
