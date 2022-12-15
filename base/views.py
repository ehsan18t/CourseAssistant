from django.shortcuts import render

from .forms import CreateUserForm as UserCreationForm
from .forms import LoginForm
from .models import User


# Create your views here.
def home(request):
    data = User.objects.all()
    return render(request, 'home.html', {'data': data})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            return render(request, 'home.html')
    return render(request, 'login.html', {'form': form})


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html')
    return render(request, 'signup.html', {'form': form})


def messages(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')
