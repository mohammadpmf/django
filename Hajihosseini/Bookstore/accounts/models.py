from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_FEMALE = 'f'
    GENDER_MALE = 'm'
    GENDER_CHOICES =(
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
    )
    nat_code = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    