from django.shortcuts import render
from .forms import CreateUserForm as UserCreationForm

from base.models import User


# Create your views here.
def home(request):
    data = User.objects.all()
    return render(request, 'home.html', {'data': data})


def login(request):
    email = request.POST.get('email')
    passwords = request.POST.get('passwords')
    if email and passwords:
        user = User.objects.filter(email=email).values()
        if user and user.passwords == passwords:
            return render(request, 'home.html')
        else:
            return render(request, 'login.html', {'email': email, 'passwords': passwords})
    return render(request, 'login.html')


def signup(request):
    form = {'form': UserCreationForm()}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html')
        else:
            return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', form)


def messages(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')
