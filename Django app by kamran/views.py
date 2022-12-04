from django.shortcuts import render
from django.http import HttpResponse
from .models import person , content, details


# Create your views here.

def home(request):

    if request.method=='POST' :
        type= request.POST['type']
        name= request.POST['name']
        print(type,name)

        obj=details() 
        obj.type=type
        obj.name=name
        obj.save()


        #fetch data from database

    from django.core import serializers
    data=serializers.serialize("python",details.objects.all())   

    contentss=serializers.serialize("python",content.objects.all())

    context = {
        'data': data,
        'c': contentss,
    }
    




    return render(request,'homepage by kamran flex.html',context)



def add(request):
    val1= int(request.POST['num1'])
    val2= int(request.POST['num2'])
    res=val1+val2
    return render(request,'add.html',{'result': res})    
      