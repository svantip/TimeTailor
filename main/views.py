from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .forms import *

# Create your views here.
@login_required
def homepage(request):
    return render(request, "homepage.html")


class CombinedListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_context(request)

    def post(self, request, *args, **kwargs):
        form = QuickAddTask(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Task added successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your submission.")
            context = self.get_context_data(request)
            context['form'] = form  # Update the context with the bound form (including errors)
            context['form_errors'] = True  # Add a flag to indicate form errors
            return render(request, 'homepage.html', context)

    def get_context_data(self, request):
        current_user = request.user
        return {
                'sidebar_list': Task.objects.filter(user=current_user, is_quick_add=True),
                'sidebar_list2': Task.objects.filter(user=current_user, is_completed=True),
                'main_list': Task.objects.filter(user=current_user),
                'form': QuickAddTask(),  # Initialize a new form for normal get requests
            }

    def render_context(self, request):
        context = self.get_context_data(request)
        return render(request, 'homepage.html', context)
    
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



