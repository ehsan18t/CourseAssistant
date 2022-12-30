from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUserForm as UserCreationForm
from .forms import LoginForm
from .models import *


# Create your views here.
def install_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        uni_name = request.POST.get('uni_name')
        domain = request.POST.get('domain')
        sid = request.POST.get('sid_pattern')
        email_pattern = request.POST.get('email_pattern')
        dept = request.POST.get('dept')
        
        #  Create University
        uni = University.objects.create(name=uni_name, domain=domain, sid_pattern=sid, email_pattern=email_pattern)
        uni.save()
        uni = University.objects.first()

        # Create Department
        dept = Department.objects.create(name=dept, university=uni)
        dept.save()
        dept = Department.objects.first()

        # Create Admin
        user = User.objects.create_superuser(email=email, password=password1, first_name=first_name, last_name=last_name, username=sid, department=dept, university=uni, is_staff=True, is_superuser=True, is_active=True)
        user.save()

        return redirect('login')

    return render(request, check_uni_for_admin_creation())


def check_uni_for_admin_creation():
    return 'install/install.html' if University.objects.first() is None else 'install/error.html'


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


# @login_required(login_url='login')
# def messages_page(request):
#     return render(request, 'messages.html')


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



@login_required(login_url='login')
def home(request):
    user = request.user
    content = Content.objects.filter(approved=True, university=user.university, department=user.department)
    reactions = []
    comments = []
    for c in content:
        reaction = Reaction.objects.filter(content=c)
        like = reaction.filter(reaction=1).count()
        dislike = reaction.filter(reaction=2).count()
        reactions.append({'like': like, 'dislike': dislike})
        comments.append(Comment.objects.filter(content=c).count())
    data = zip(content, reactions, comments)
    return render(request, 'home.html', {'data': data})

