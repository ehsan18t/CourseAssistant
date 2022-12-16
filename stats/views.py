from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Semester


@login_required(login_url='login')
def stats(request):
    if request.method == 'POST':
        if 'add_semester' in request.POST:
            add_semester(request)
        if 'delete_semester' in request.POST:
            delete_semester(request)
        return redirect('stats')
    data = Semester.objects.filter(user=request.user)
    return render(request, 'stats/stats.html', {'data': data})


def add_semester(request):
    semester = request.POST.get('semester_name')
    start_date = request.POST.get('semester_start_date')
    end_date = request.POST.get('semester_end_date')

    is_running = request.POST.get('is_semester_running')
    if is_running == 'on':
        is_running = True
    else:
        is_running = False

    auto_add_to_group = request.POST.get('auto_add_to_group')
    if auto_add_to_group == 'on':
        auto_add_to_group = True
    else:
        auto_add_to_group = False

    user = request.user

    obj = Semester(name=semester, start_date=start_date, end_date=end_date, is_running=is_running,
                   auto_add_to_group=auto_add_to_group, user=user)
    obj.save()


def delete_semester(request):
    semester_id = request.POST.get('semester_id')
    sem = Semester.objects.filter(id=semester_id)
    if request.user == sem[0].user:
        sem.delete()
    else:
        print('Error: User not authorized to delete this semester')
