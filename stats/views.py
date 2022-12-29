import copy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Semester, Course, Assessment, Assessment_Type
from chat.models import Study_Group, Participant


def marks_to_gpa(marks):
    gpa = {'55': 00, '58': 1.00, '62': 1.33, '66': 1.67, '70': 2.00, '74': 2.33, '78': 2.67, '82': 3.00, '83': 3.33, '86': 3.33, '90': 3.67, '101': 4.00}
    for i in gpa:
        if int(marks) <= int(i):
            return gpa[i]


@login_required(login_url='login')
def stats(request):
    if request.method == 'POST':
        if 'add_semester' in request.POST:
            add_semester(request)
        if 'delete_semester' in request.POST:
            delete_semester(request)
        return redirect('stats')
    semester = Semester.objects.filter(user=request.user)
    labels = []
    for sem in semester:
        labels.append(sem.name)
    gpa = []
    ex_gpa = []
    ob_gpa = []
    for sem in semester:
        courses = Course.objects.filter(semester=sem.id)
        ex = 0.0
        ob = 0.0
        to = 0.0
        for course in courses:
            parts = Assessment.objects.filter(course=course.id)
            for p in parts:
                ex += p.expected_marks
                ob += p.obtained_marks
                to += p.total_marks
        if to != 0:
            ex = (ex/to)*100
            ob = (ob/to)*100
        gpa.append({'expected': marks_to_gpa(ex), 'obtained': marks_to_gpa(ob)})
        ex_gpa.append(marks_to_gpa(ex))
        ob_gpa.append(marks_to_gpa(ob))
    data = zip(semester, gpa)
    chart = {'labels': labels, 'expected': ex_gpa, 'obtained': ob_gpa}
    return render(request, 'stats/stats.html', {'data': data, 'chart': chart})


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
        if 'create_group' in request.POST:
            create_study_group(request)
        if 'join_group' in request.POST:
            join_study_group(request)
        return redirect('courses', pk=pk)

    data = Course.objects.filter(semester=pk)
    names = []
    for course in data:
        names.append(course.name)
    assessments = []
    groups = []
    marks = []
    user_exists_in_group = []
    for course in data:
        g = if_group_exists(course)
        groups.append(g)
        user_exists_in_group.append(if_user_in_group(request.user, g))
        parts = Assessment.objects.filter(course=course.id)
        ex = 0.0
        ob = 0.0
        to = 0.0
        for p in parts:
            ex += p.expected_marks
            ob += p.obtained_marks
            to += p.total_marks
        if to != 0:
            ex = (ex/to)*100
            ob = (ob/to)*100
        assessments.append({'expected': round(ex, 2), 'obtained': round(ob, 2)})
        marks.append(round(ob, 2))
    data = zip(data, assessments, groups, user_exists_in_group)
    chart = {'labels': names, 'marks': marks}
    semester_obj = Semester.objects.filter(id=pk)[0]
    return render(request, 'stats/courses.html', {'data': data, 'semester': pk, 'semester_obj': semester_obj, 'chart': chart})


def if_user_in_group(user, group):
    if group is None:
        return False
    else:
        return len(Participant.objects.filter(user=user, study_group=group)) != 0


def if_group_exists(course):
    user = course.semester.user
    group = Study_Group.objects.filter(course_code=course.course_code, section=course.section, university=user.university)
    if len(group) == 0:
        return None
    else:
        return group[0]


def auto_add_people_to_group(course, group):
    university  = course.semester.user.university
    courses = Course.objects.filter(course_code=course.course_code, section=course.section)
    accepted = []
    for  c in courses:
        if c.semester.auto_add_to_group and c.semester.is_running:
            accepted.append(c.semester.user)
    for user in accepted:
        if user.university == university:
            obj = Participant(user=user, study_group=group)
            obj.save()


def create_study_group(request):
    university = request.user.university
    course_id = request.POST.get('course_id')
    course = Course.objects.filter(id=course_id)[0]
    # group = Study_Group.objects.filter(course=course_id)
    # if len(group) == 0:
    obj = Study_Group(name=f'{course.course_code} - {course.name} [{course.section}]', course_code=course.course_code, university = university, section=course.section)
    obj.save()
    obj = Participant(user=request.user, study_group=obj)
    obj.save()
    auto_add_people_to_group(course, obj.study_group)


def join_study_group(request):
    course_id = request.POST.get('course_id')
    course = Course.objects.filter(id=course_id)[0]
    group = Study_Group.objects.filter(course_code=course.course_code, section=course.section)[0]
    obj = Participant(user=request.user, study_group=group)
    obj.save()


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

    obj = Course(name=course, course_code=course_code, section=course_section, credit=end_date, semester_id=semester,
                 is_retake=is_retake)
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
    return render(request, 'stats/assessments.html',
                  {'data': data, 'assessment_types': assessment_types, 'semester': s_pk, 'course': c_pk})


def add_assessment(request):
    name = request.POST.get('assessment_name')
    assessment_type = Assessment_Type.objects.filter(id=request.POST.get('assessment_type'))[0]
    total_marks = request.POST.get('total_marks')
    expected_marks = request.POST.get('expected_marks')
    obtained_marks = request.POST.get('obtained_marks')
    course = Course.objects.filter(id=request.POST.get('course_id'))[0]

    obj = Assessment(name=name, assessment_type=assessment_type, total_marks=total_marks, expected_marks=expected_marks,
                     obtained_marks=obtained_marks, course=course)
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
