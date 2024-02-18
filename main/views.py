

import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
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
from datetime import datetime

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
            task_id = request.POST.get('task_id')
            if task_id:
                task_instance = get_object_or_404(Task, id=task_id, user=request.user)
                form = QuickAddTask(request.POST, instance=task_instance, user=request.user)
            else:
                form = QuickAddTask(request.POST, user=request.user)

            if form.is_valid():
                form.save()
                message = "Task updated successfully." if task_id else "Quick task added successfully."
                messages.success(request, message)
                return redirect(reverse('home'))
            else:
                messages.error(request, "There was an error with your submission.")
        elif 'submit_start_time' in request.POST:
            form = StartTimeForm(request.POST, user=request.user)  # Assuming StartTimeForm is correctly defined
            if form.is_valid():
                form.save()
                messages.success(request, "Start time set successfully.")
                return redirect(reverse('home'))
            else:
                messages.error(request, "There was an error with setting the start time.")
        elif 'submit_task_add' in request.POST:
            task_id = request.POST.get('task_id', None)  # Get the task ID from the form, if it exists
            task_instance = Task.objects.filter(id=task_id).first() if task_id else None  # Fetch the task if ID exists
            
            form = AddTaskForm(request.POST, instance=task_instance, user=request.user)  # Initialize form with instance if updating
            
            if form.is_valid():
                form.save()
                message = "Task updated successfully." if task_id else "Task added successfully."
                messages.success(request, message)
                return redirect(reverse('home'))
            else:
                messages.error(request, "There was an error with the task form.")      
        
        
        # If neither form is valid, or if another POST request without form submission
        context = self.get_context_data()
        context['form'] = form  # You may need to handle this more gracefully for multiple forms
        context['form_errors'] = True
        return render(request, 'homepage.html', context)

    def get_context_data(self):
        current_user = self.request.user
        quick_add_tasks = Task.objects.filter(user=current_user, is_quick_add=True)
        completed_tasks = Task.objects.filter(user=current_user, is_completed=True, date=datetime.today())
        all_tasks = Task.objects.filter(user=current_user, is_completed=False)
        form_quick_add = QuickAddTask(user=current_user)  # Initialize form with user for GET requests
        form_start_time = StartTimeForm() 
        form_add_task = AddTaskForm(user=current_user)
        return {
            'sidebar_list': quick_add_tasks,
            'sidebar_list2': completed_tasks,
            'main_list': all_tasks,
            'form_quick_add': form_quick_add,
            'form_start_time': form_start_time,
            'form_add_task' : form_add_task,
            'hours_range': range(24),
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
    tasks = Task.objects.filter(user=request.user, date=selected_date, is_quick_add=False, is_completed = False)
    
    # Serialize tasks to JSON
    tasks_json = serialize('json', tasks, fields=('name', 'start_time', 'duration', 'icon', 'color'))
    
    return JsonResponse({'tasks': tasks_json}, safe=False)

def update_task_completion(request, task_id):
    try:
        # Parse the JSON body
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        completed = body.get('completed', False)

        # Retrieve and update the task
        task = Task.objects.get(pk=task_id)
        task.is_completed = True
        task.save()
       

        # Return a success response
        return JsonResponse({"message": "Task updated successfully."})

    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."}, status=404)
    except Exception as e:
        return HttpResponseBadRequest({"error": str(e)})
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure the task belongs to the user
    task.delete()
    return JsonResponse({'status': 'success'}, status=200)

