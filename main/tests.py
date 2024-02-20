from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, QuickAddTask, AddTaskForm, StartTimeForm
from .models import Task
from .views import *
import datetime


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

    
class ViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        # Create a task
        self.task = Task.objects.create(
            name='Test Task',
            user=self.user,
            date=datetime.date.today(),
            is_quick_add=True,
            duration=datetime.timedelta(minutes=60) 
        )

        
    def test_login_required_to_access_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/auth/login/?next={reverse("home")}')

    def test_authenticated_access_to_homepage(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_delete_task(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        
    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpassword', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        
    def test_update_task_completion(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.patch(reverse('update_task_completion', args=[self.task.id]), {'completed': True}, content_type='application/json')
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)