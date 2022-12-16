from django.shortcuts import render
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return render(request, 'home.html')


def messages(request):
    return render(request, 'messages.html')


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


