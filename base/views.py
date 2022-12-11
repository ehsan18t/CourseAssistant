from django.shortcuts import render

from base.models import User


# Create your views here.
def home(request):
    data = User.objects.all()
    return render(request, 'home.html', {'data': data})


def messages(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')
