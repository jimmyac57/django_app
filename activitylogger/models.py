from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TimeLogger(models.Model):
    activity = models.CharField(max_length=200)
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

