# forms.py
from datetime import timedelta
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
    class Meta:
        model = Task
        fields = ['name', 'icon', 'duration', 'color']

    def save(self, commit=True, user=None):
        instance = super(QuickAddTask, self).save(commit=False)
        # Convert hours and minutes to a duration
        hours = self.cleaned_data.get('taskDurationHours', 0)
        minutes = self.cleaned_data.get('taskDurationMinutes', 0)
        instance.duration = timedelta(hours=hours, minutes=minutes)
        if user:
            instance.user = user
        instance.is_quick_add = True
        if commit:
            instance.save()
        return instance