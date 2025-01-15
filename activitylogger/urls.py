from django.urls import path
from . import views

urlpatterns = [
   path('log/', views.activityLogger, name='activity_logger'),
   path('endActivity/<int:id>', views.endActivity, name='end_activity'),
]