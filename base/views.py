from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm as UserCreationForm
from .forms import LoginForm
from .models import User


# Create your views here.
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


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
    return render(request, 'signup.html', {'form': form})


def messages_page(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')
