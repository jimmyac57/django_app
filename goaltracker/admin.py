from django.contrib import admin

# Register your models here.
from .models import Goal
from .models import Objective
from .models import ProgressRecord

admin.site.register(Goal)
admin.site.register(Objective)
admin.site.register(ProgressRecord)
