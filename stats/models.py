from django.db import models

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_running = models.BooleanField(default=False)
    auto_add_to_group = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    course_code = models.CharField(max_length=20)
    credit = models.IntegerField()
    section = models.CharField(max_length=20)
    semester = models.ForeignKey(Semester)
    is_retake = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course)
    total_marks = models.FloatField()
    expected_marks = models.FloatField()
    date = models.DateField()   # not using now, but maybe in future

    def __unicode__(self):
        return self.name

class Assessment_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    mark_percentage = models.FloatField()
    best_of = models.IntegerField()
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.name
