from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUserForm as UserCreationForm
from .forms import LoginForm
from .models import User,Content,Content_Request

"""
# Create your views here.
@login_required(login_url='login')
def home(request):
    data = User.objects.all()
    return render(request, 'home.html', {'data': data})
"""    


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


contexts = [
        {
        "course": "Datastructur and Algorithm",
        "con": "Ashik ",
        "file": "ct2.pdf",
        "desc": "ct2, faculty: FTI asdfasd asdf a             asdfsdf asdf asdf asdf asdf asdf",
        "id": "1"
        },
        {
        "course": "System Analysis and Design",
        "con": "Kamran",
        "file": "slide1.pdf",
        "desc": "covers lecture upto 3rd class",
        "id": "3"
        },
        {
        "course": "Computer Architercure",
        "con": "Sharif ",
        "file": "slide3.pdf",
        "desc": "topics: Pipeline and MIPS code",
        "id": "2"
        },
        {
        "course": "System Analysis and Design",
        "con": "Karim",
        "file": "slide2.pdf",
        "desc": "covers lecture upto 3rd class",
        "id": "4"
        },
        {
        "course": "Fundamenta Calc",
        "con": "Ahsan",
        "file": "slide1.pdf",
        "desc": "covers lecture upto 3rd class",
        "id": "5"
        },
        {
        "course": "System Analysis and Design",
        "con": "Ashik",
        "file": "mid.pdf",
        "desc": "midterm fall 2020",
        "id": "6"
        },
        {
        "course": "Microcontroller",
        "con": "Asif",
        "file": "presentation1.pdf",
        "desc": "our presentation on Django",
        "id": "7"
        },
        {
        "course": "Microcontroller",
        "con": "Asif",
        "file": "presentation1.pdf",
        "desc": "our presentation on Django",
        "id": "8"
        },
        {
        "course": "Microcontroller",
        "con": "Asif",
        "file": "presentation1.pdf",
        "desc": "our presentation on Django",
        "id": "9"
        },
        
        {
        "course": "Computer Architucture",
        "con": "Tabarak",
        "file": "mid.pdf",
        "desc": "mid term question, fall 2020",
        "id": "10"
        }
    ]

def content_approval(request):
    
    global contexts
    if request.method == 'POST' :
        whichBtn = request.POST.get('btn')
        isAll = request.POST.getlist('allSelected')
        checkedItems = request.POST.getlist('checkBox')
        

        if whichBtn == 'approve':
            print('approve is selected')
            for i in checkedItems:
                contexts = [j for j in contexts if not ((j['id']) == i)]
        else :
            print('delete is selected')
            for i in checkedItems:
                contexts = [j for j in contexts if not ((j['id']) == i)]
        

    paginator = Paginator(contexts, 4) # Show 1 data set per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'content_approval.html', {'page_obj': page_obj})










def home(request):
    #fetch data from database

    from django.core import serializers
    contents=serializers.serialize("python",Content.objects.all()) 

    context = {
        
        'c': contents,
    }
    


    return render(request, 'home.html',context)



def request_content(request):
    #save data in  database
    if request.method=="POST" :
        title=request.POST['title']
        code=request.POST['course_code']
        semester=request.POST['semester']
        description=request.POST['description']
       

        

        if len(title)!=0 and len(code)!=0  and len(semester)!=0  and len(description)!=0 :
          obj=Content_Request()  
          obj.course_name=title
          obj.course_code=code
          obj.semester=semester
          obj.description=description

          obj.save() 

       
   
    


    return render(request, 'content_request.html')






def site_setting(request):
  
    if request.method=="POST" :
        name=request.POST['name']
        email_pattern=request.POST['email_pattern']
        sid_pattern=request.POST['sid_pattern']
        
       

        

        if len(name)!=0 and len(sid_pattern)!=0  and len(email_pattern)!=0  :
          obj=University()  
          obj.name=name
          obj.email_pattern=email_pattern
          obj.sid_pattern=sid_pattern
          

          obj.save() 

    
       
        
        
        
          

                




    #fetch data from database

    from django.core import serializers
    contentss=serializers.serialize("python",University.objects.all()) 

    context = {
        
        'c': contentss,
    }
    


    return render(request, 'site_settings.html',context)






def delete_university(request):
    print("I am here in delete university")
    
    if request.method=="POST" :
       selected_name=request.POST['university']
       from django.core import serializers
       University.objects.filter(name=selected_name).delete()
       print("finally deleted")
       
       
    #fetch data from database

    from django.core import serializers
    contentss=serializers.serialize("python",University.objects.all()) 

    context = {
        
        'c': contentss,
    }
    
    
    


    return render(request, 'delete_university.html',context)












   
     
def content_view(request):

    if request.method == 'POST':
        c = request.POST['comment']
       
        obj=comment()  
        obj.comment=c
        obj.save()
        

    from django.core import serializers
    contentss=serializers.serialize("python",content.objects.all()) 
    comments=serializers.serialize("python",comment.objects.all()) 
     

    context = {
        
        'c': contentss,
        'cmnt': comments,
    }
    



    return render(request, 'content_view.html',context)


