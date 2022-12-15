from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUserForm as UserCreationForm
from .forms import LoginForm
from .models import User


# Create your views here.
@login_required(login_url='login')
def home(request):
    data = User.objects.all()
    return render(request, 'home.html', {'data': data})


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('passwords')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def messages_page(request):
    return render(request, 'messages.html')


@login_required(login_url='login')
def chat(request):
    return render(request, 'chat.html')
