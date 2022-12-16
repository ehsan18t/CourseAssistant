from django.shortcuts import render

from .models import Semester


def stats(request):
    if request.method == 'POST' and 'add_semester' in request.POST:
        add_semester(request)
    data = Semester.objects.all()
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

    obj = Semester(name=semester, start_date=start_date, end_date=end_date, is_running=is_running, auto_add_to_group=auto_add_to_group)
    obj.save()