from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

# Create your models here.
class TimeLogger(models.Model):
    activity = models.CharField(max_length=200)
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.time_start and self.time_end:
            self.duration = self.time_end - self.time_start
        else:
            self.duration = None
        super().save(*args, **kwargs)

    def formatted_duration(self):
        if self.duration:
            total_seconds = int(self.duration.total_seconds())
            days, remainder = divmod(total_seconds, 86400)  
            hours, remainder = divmod(remainder, 3600)     
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                return f"{days} day{'s' if days > 1 else ''}, {hours}:{minutes:02}:{seconds:02}"
            else:
                return f"{hours:02}:{minutes:02}:{seconds:02}"
        return "Not available"

