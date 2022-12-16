from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Semester, Course, Assessment, Assessment_Type


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


@login_required(login_url='login')
def courses(request, pk):
    if request.method == 'POST':
        if 'add_course' in request.POST:
            add_course(request)
        if 'delete_course' in request.POST:
            delete_course(request)
        return redirect('courses', pk=pk)

    data = Course.objects.filter(semester=pk)
    return render(request, 'stats/courses.html', {'data': data, 'semester': pk})


def add_course(request):
    course = request.POST.get('course_name')
    course_code = request.POST.get('course_code')
    course_section = request.POST.get('course_section')
    end_date = request.POST.get('course_credit')
    semester = request.POST.get('semester_id')

    is_retake = request.POST.get('is_retake')
    if is_retake == 'on':
        is_retake = True
    else:
        is_retake = False

    obj = Course(name=course, course_code=course_code, section=course_section, credit=end_date, semester_id=semester, is_retake=is_retake)
    obj.save()


def delete_course(request):
    course_id = request.POST.get('course_id')
    course = Course.objects.filter(id=course_id)[0]
    semester = Semester.objects.filter(id=course.semester_id)[0]
    if request.user == semester.user:
        course.delete()
    else:
        print('Error: User not authorized to delete this course')


@login_required(login_url='login')
def assessments(request, s_pk, c_pk):
    if request.method == 'POST':
        if 'add_assessment' in request.POST:
            add_assessment(request)
        if 'delete_assessment' in request.POST:
            delete_assessment(request)
        return redirect('assessments', s_pk=s_pk, c_pk=c_pk)
    data = Assessment.objects.filter(course=c_pk)
    assessment_types = Assessment_Type.objects.filter(course=c_pk)
    return render(request, 'stats/assessments.html', {'data': data, 'assessment_types': assessment_types, 'semester': s_pk, 'course': c_pk})


def add_assessment(request):
    name = request.POST.get('assessment_name')
    assessment_type = Assessment_Type.objects.filter(id=request.POST.get('assessment_type'))[0]
    total_marks = request.POST.get('total_marks')
    expected_marks = request.POST.get('expected_marks')
    obtained_marks = request.POST.get('obtained_marks')
    course = Course.objects.filter(id=request.POST.get('course_id'))[0]

    obj = Assessment(name=name, assessment_type=assessment_type, total_marks=total_marks, expected_marks=expected_marks, obtained_marks=obtained_marks, course=course)
    obj.save()


def delete_assessment(request):
    assessment_id = request.POST.get('assessment_id')
    assessment = Assessment.objects.filter(id=assessment_id)
    course = Course.objects.filter(id=assessment.course_id)[0]
    semester = Semester.objects.filter(id=course.semester_id)[0]
    if request.user == semester.user:
        assessment.delete()
    else:
        print('Error: User not authorized to delete this assessment')


@login_required(login_url='login')
def assessment_types(request, s_pk, c_pk):
    if request.method == 'POST':
        if 'add_assessment_type' in request.POST:
            add_assessment_type(request)
        if 'delete_assessment_type' in request.POST:
            delete_assessment_type(request)
        return redirect('assessment-types', s_pk=s_pk, c_pk=c_pk)

    data = Assessment_Type.objects.filter(course=c_pk)
    return render(request, 'stats/assessment_types.html', {'data': data, 'semester': s_pk, 'course': c_pk})


def add_assessment_type(request):
    name = request.POST.get('assessment_type_name')
    mark_percentage = request.POST.get('mark_percentage')
    best_of = request.POST.get('best_of')
    course = Course.objects.filter(id=request.POST.get('course_id'))[0]

    obj = Assessment_Type(name=name, mark_percentage=mark_percentage, best_of=best_of, course=course)
    obj.save()


def delete_assessment_type(request):
    assessment_type_id = request.POST.get('assessment_type_id')
    assessment_type = Assessment_Type.objects.filter(id=assessment_type_id)[0]
    course = assessment_type.course
    semester = Semester.objects.filter(id=course.semester_id)[0]
    if request.user == semester.user:
        assessment_type.delete()
    else:
        print('Error: User not authorized to delete this assessment type')
