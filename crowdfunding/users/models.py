from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = [("mentor","Mentor"),
                  ("mentee","Mentee")]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        null=False,
        blank=False
    )
    def __str__(self):
        return self.username
