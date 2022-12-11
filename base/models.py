from django.db import models


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    email_pattern = models.CharField(max_length=100)  # university pattern
    sid_pattern = models.CharField(max_length=100)  # student id pattern

    def __str__(self):
        return f'{self.name} {self.domain} ({self.email_pattern}) - {self.sid_pattern}'


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

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.s_id}) - {self.university.name}'
