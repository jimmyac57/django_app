from django.contrib import admin

# Register your models here.
from .models import TimeLogger
from django.utils.timezone import localtime

@admin.register(TimeLogger)
class TimeLoggerAdmin(admin.ModelAdmin):
    list_display = ('activity', 'time_start', 'time_end', 'formatted_duration', 'user')
    list_filter = ('activity', 'time_start', 'time_end', 'user')
    search_fields = ('activity', 'user__username')
    date_hierarchy = 'time_start'
    ordering = ('-time_start',)
    actions = ['mark_as_finished']
    
    def mark_as_finished(self, request, queryset):
        queryset.update(time_end=localtime())
    mark_as_finished.short_description = "Mark selected activities as finished"
