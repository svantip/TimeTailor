# forms.py
from datetime import time, timedelta
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        

class QuickAddTask(forms.ModelForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    duration_hours = forms.IntegerField(min_value=0, max_value=24, required=True)
    duration_minutes = forms.IntegerField(min_value=0, max_value=59, required=True)

    class Meta:
        model = Task
        fields = ['name', 'icon', 'color']  # 'duration' is handled separately
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuickAddTask, self).__init__(*args, **kwargs)

    def clean_duration(self):
        duration_hours = self.cleaned_data.get('duration_hours', 0)
        duration_minutes = self.cleaned_data.get('duration_minutes', 0)
        return timedelta(hours=duration_hours, minutes=duration_minutes)
    
    def save(self, commit=True):
        task_id = self.cleaned_data.get('task_id')
        if task_id:
            instance = Task.objects.get(id=task_id)  # Get the existing task instance
        else:
            instance = Task()  # Create a new instance if no ID

        # Set instance fields from form fields
        instance.name = self.cleaned_data.get('name')
        instance.icon = self.cleaned_data.get('icon')
        instance.color = self.cleaned_data.get('color')
        instance.duration = self.clean_duration()
        instance.is_quick_add = True
        instance.user = self.user if self.user else None
        instance.start_time = None
        instance.repeat_frequency = None
        instance.is_completed = False
        instance.date = None

        if commit:
            instance.save()
        return instance
    
    
    
class AddTaskForm(forms.ModelForm):
    duration_hours = forms.IntegerField(min_value=0, max_value=24, required=True)
    duration_minutes = forms.IntegerField(min_value=0, max_value=59, required=True)

    class Meta:
        model = Task
        fields = ['name', 'icon', 'color', 'start_time', 'is_quick_add', 'date']  # 'duration' is handled separately
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddTaskForm, self).__init__(*args, **kwargs)

    def clean_duration(self):
        duration_hours = self.cleaned_data.get('duration_hours', 0)
        duration_minutes = self.cleaned_data.get('duration_minutes', 0)
        return timedelta(hours=duration_hours, minutes=duration_minutes)
    
    def save(self, commit=True):
        instance = super(AddTaskForm, self).save(commit=False)
        instance.duration = self.clean_duration()  # Ensure this is correctly set
        instance.is_quick_add = False
        if self.user:
            instance.user = self.user
        instance.repeat_frequency = None
        instance.is_completed = False
        instance.date = self.cleaned_data.get('date', datetime.today())
        
        if commit:
            instance.save()
        return instance
    

class StartTimeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'icon', 'color', 'duration', 'start_time', 'is_quick_add', 'date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(StartTimeForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(StartTimeForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        instance.date = self.cleaned_data.get('date', datetime.today())  # Default to today if no date is provided
        instance.repeat_frequency = None
        instance.is_completed = False
        
        if commit:
            instance.save()
        return instance