from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def messages(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')

def content_approval(request):
    return render(request, 'content_approval.html')
