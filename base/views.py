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


def content_approval(request):
    
    contexts = Content.objects.filter(approved=False)
    if request.method == 'POST' :
        whichBtn = request.POST.get('btn')
        isAll = request.POST.getlist('allSelected')
        checkedItems = request.POST.getlist('checkBox')
        

        if whichBtn == 'approve':
            print('approve is selected')
            for i in checkedItems:
                context = Content.objects.get(id=i)
                context.approved = True
                context.save()
        else :
            print('delete is selected')
            for i in checkedItems:
                context = Content.objects.get(id=i)
                context.delete()
        

    paginator = Paginator(contexts, 4) # Show 1 data set per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'content_approval.html', {'page_obj': page_obj})



def fetch_data_of_content(content):
    reaction = Reaction.objects.filter(content=content)
    like = reaction.filter(reaction=1).count()
    dislike = reaction.filter(reaction=2).count()
    reaction = {'like': like, 'dislike': dislike}
    comments = Comment.objects.filter(content=content)
    return reaction, comments



@login_required(login_url='login')
def home(request):
    user = request.user
    if request.method == 'POST':
        if 'add_reaction' in request.POST:
            pk = request.POST.get('pk')
            reaction = request.POST.get('reaction')
            add_reaction(request, pk, reaction)
        if 'add_content' in request.POST:
            title = request.POST.get('title')
            course_code = request.POST.get('course_code')
            description = request.POST.get('description')
            file = request.FILES.get('file')
            thumbnail = request.FILES.get('thumbnail')
            add_content(request, title, course_code, description, file, thumbnail)

        return redirect('home')

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


def add_content(request, title, course_code, description, file, thumbnail):
    user = request.user
    university = user.university
    department = user.department
    Content.objects.create(title=title, course_code=course_code, description=description, file=file, thumbnail=thumbnail,
                           user=user, university=university, department=department)

def add_reaction(request, pk, reaction):
    content = Content.objects.filter(id=pk)[0]
    user = request.user

    # if exist then check if same reaction or not
    if Reaction.objects.filter(content=content, user=user).exists():
        r = Reaction.objects.filter(content=content, user=user)[0]
        if r.reaction == int(reaction): # if same reaction then delete
            r.reaction = reaction
            r.delete()
        else:   # if not same reaction then update
            r.reaction = reaction
            r.save()
    else:
        Reaction.objects.create(content=content, user=user, reaction=reaction)


@login_required(login_url='login')
def content_view(request, pk):
    if request.method == 'POST':
        if 'add_comment' in request.POST:
            add_comment(request, pk)
        if 'add_reply' in request.POST:
            r_pk = request.POST.get('comment_id')
            add_reply(request, r_pk, pk)
        return redirect('content_view', pk=pk)
    content = Content.objects.filter(id=pk)[0]
    reaction, comments = fetch_data_of_content(content)
    return render(request, 'content_view.html', {'content': content, 'reaction': reaction, 'comments': comments})


def add_comment(request, pk):
    content = Content.objects.filter(id=pk)[0]
    user = request.user
    comment = request.POST.get('comment')
    Comment.objects.create(content=content, user=user, text=comment)


def add_reply(request, r_pk, pk):
    comment = Comment.objects.filter(id=r_pk)[0]
    content = Content.objects.filter(id=pk)[0]
    user = request.user
    reply = request.POST.get('reply')
    Comment.objects.create(content=content, user=user, text=reply, parent=comment)