from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        app_label = 'accounts' 