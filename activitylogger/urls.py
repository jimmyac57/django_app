from django.urls import path
from . import views

urlpatterns = [
   path('logs/', views.activityLogger, name='activity_logger'),
   path('endActivity/<int:id>', views.endActivity, name='end_activity'),
   path('api/currentHour/', views.currentHour, name='current_hour'),
   path('logs/finished/', views.finishedActivities, name='finished_activities'),
   path('logs/add_activity/', views.addActivity, name='add_activity'),

]