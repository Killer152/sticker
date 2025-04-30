from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'user'
