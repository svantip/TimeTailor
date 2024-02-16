
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .forms import *
from django.core.serializers import serialize

# Create your views here.
@login_required
def homepage(request):
    return render(request, "homepage.html")



class CombinedListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'homepage.html', context)

    def post(self, request, *args, **kwargs):
        # Check which form was submitted
        if 'submit_quick_add' in request.POST:
            form = QuickAddTask(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Task added successfully.")
                return redirect(reverse('home'))
            else:
                messages.error(request, "There was an error with your Quick Add submission.")
        elif 'submit_start_time' in request.POST:
            form = StartTimeForm(request.POST, user=request.user)  # Assuming StartTimeForm is correctly defined
            if form.is_valid():
                form.save()
                messages.success(request, "Start time set successfully.")
                return redirect(reverse('home'))
            else:
                messages.error(request, "There was an error with setting the start time.")
        
        # If neither form is valid, or if another POST request without form submission
        context = self.get_context_data()
        context['form'] = form  # You may need to handle this more gracefully for multiple forms
        context['form_errors'] = True
        return render(request, 'homepage.html', context)

    def get_context_data(self):
        current_user = self.request.user
        quick_add_tasks = Task.objects.filter(user=current_user, is_quick_add=True)
        completed_tasks = Task.objects.filter(user=current_user, is_completed=True)
        all_tasks = Task.objects.filter(user=current_user)
        form_quick_add = QuickAddTask(user=current_user)  # Initialize form with user for GET requests
        form_start_time = StartTimeForm()  # Assuming this form does not need the user passed in
        return {
            'sidebar_list': quick_add_tasks,
            'sidebar_list2': completed_tasks,
            'main_list': all_tasks,
            'form_quick_add': form_quick_add,
            'form_start_time': form_start_time,
        }
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            context = {"message":"Passwords do not match"}
            return render(request, 'signup.html', context)

        if User.objects.filter(username=username).exists():
            context = {"message":"Username already exists"}
            return render(request, 'signup.html', context)

        if User.objects.filter(email=email).exists():
            context = {"message":"Email already exists"}
            return render(request, 'signup.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/') 

    return render(request, 'signup.html')

def login_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:   
            message = "Check your credentials. We didn't find a match!"
    
    context={'message':message}
    return render(request, 'login.html', context)

@login_required
def get_tasks_for_date(request, date_str):
    # Convert the date_str to a date object
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    tasks = Task.objects.filter(user=request.user, date=selected_date, is_quick_add=False)
    
    # Serialize tasks to JSON
    tasks_json = serialize('json', tasks, fields=('name', 'start_time', 'duration'))
    
    return JsonResponse({'tasks': tasks_json}, safe=False)


