from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desired_identity = models.CharField(max_length=100)  
    desired_result = models.CharField(max_length=100)    
    system = models.CharField(max_length=200)         
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateField(null=True, blank=True)
  

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.desired_identity

class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]

    UNIT_CHOICES = [
        ('days', 'Days'),
        ('hours', 'Hours'),
        ('minutes', 'Minutes'),
        ('occurrences', 'Occurrences'), 
    ]

    CHART_CHOICES = [
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
        # ...
    ]

    goal = models.ForeignKey(Goal,related_name='objectives', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type_period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    value_by_period = models.IntegerField()  
    unit_of_value = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='occurrences'
    )
    chart = models.CharField(
        max_length=10,
        choices=CHART_CHOICES,
        default='bar'
    )

    def __str__(self):
        return f"{self.name} ({self.goal.desired_identity})"

class ProgressRecord(models.Model):
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    value = models.IntegerField() 
    unit_of_value = models.CharField(max_length=20)  
    
    record_date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)  

    def __str__(self):
        return f"Progress of {self.value} for {self.objective.name}"
