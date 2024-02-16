from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)  
    color = models.CharField(max_length=7)  
    start_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField()  
    repeat_frequency = models.CharField(max_length=50, blank=True, null=True) 
    is_quick_add = models.BooleanField() 
    is_completed = models.BooleanField(default = False) 
    date = models.DateField(null = True, blank = True)

    @property
    def end_time(self):
        if self.start_time and self.duration:
            return self.start_time + self.duration
        return None

    def __str__(self):
        return self.name
    
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name