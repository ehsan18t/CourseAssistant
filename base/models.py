from django.db import models


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    email_pattern = models.CharField(max_length=100)  # university id pattern
    sid_pattern = models.CharField(max_length=100)  # student id pattern


class User(models.Model):
    id = models.AutoField(primary_key=True)
    s_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passwords = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    periods = models.IntegerField()  # 1 = trimester, 2 = Semester
