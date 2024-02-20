from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, QuickAddTask, AddTaskForm, StartTimeForm
from .models import Task

class FormTests(TestCase):
    def test_sign_up_form(self):
        form_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'abracadabra123','password1': 'abracadabra', 'password2': 'abracadabra123'}
        form = SignUpForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_quick_add_task_form(self):
        user = User.objects.create_user(username='svantip', password='tockica184')
        form_data = {'name': 'Test Task','color':'#ffffff', 'icon':'bxs-shower', 'duration_hours': 1, 'duration_minutes': 30}
        form = QuickAddTask(data=form_data, user=user)
        self.assertTrue(form.is_valid())

    def test_add_task_form(self):
        user = User.objects.create_user(username='svantip', password='tockica184')
        form_data = {'name': 'Test Task',  'color':'#ffffff','icon':'bxs-shower' , 'duration_hours': 2, 'duration_minutes': 15}
        form = AddTaskForm(data=form_data, user=user)
        self.assertTrue(form.is_valid())

    
