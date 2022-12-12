from django.shortcuts import render
from .models import content


# Create your views here.


def home(request):
    #fetch data from database

    from django.core import serializers
    contentss=serializers.serialize("python",content.objects.all()) 

    context = {
        
        'c': contentss,
    }
    


    return render(request, 'homepage.html',context)





def messages(request):
    return render(request, 'messages.html')


def chat(request):
    return render(request, 'chat.html')
