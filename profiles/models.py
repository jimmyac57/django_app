from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.jpg',blank=True)
    profile_banner = models.ImageField(upload_to='profile_banners', default='profile_banners/default.jpg',blank=True)
    about_me = models.TextField(blank=True)
    pronouns = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(blank=True, null=True)
