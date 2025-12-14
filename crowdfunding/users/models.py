from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = [("mentor","Mentor"),
                  ("mentee","Mentee")]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        null=True,
        blank=True
    )
    def save(self, *args, **kwargs):
        # Superusers don't need user_type
        if not self.is_superuser and not self.user_type:
            raise ValueError("user_type is required for non-superusers")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def is_mentor(self):
        return self.user_type == "mentor"
    
    def is_mentee(self):
        return self.user_type == "mentee"
