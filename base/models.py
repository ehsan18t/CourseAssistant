from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    email_pattern = models.CharField(max_length=100)  # university pattern
    sid_pattern = models.CharField(max_length=100)  # student id pattern

    def validate_email(self, email):
        return True
        # return email.endswith(self.email_pattern)

    def validate_sid(self, sid):
        return True
        # return sid.startswith(self.sid_pattern)

    def __str__(self):
        return f'{self.name} {self.domain} ({self.email_pattern}) - {self.sid_pattern}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.university})'


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, password, username, department, university, **other_fields):
        # Validations
        if not email:
            raise ValueError(_('You must provide an email address'))
        if university.validate_email(email) is False:
            raise ValueError(_('You must provide a valid email address'))
        if not username:
            raise ValueError(_('You must provide a student ID'))
        if university.validate_sid(username) is False:
            raise ValueError(_('You must provide a valid student ID'))

        # Normalizations and creation 
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, username=username,
                          department=department, university=university, **other_fields)
        user.set_password(password)
        user.save()
        return user


# Create user extending default user model
class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(_('Email Address'), max_length=100, unique=True)
    username = models.CharField(_('Student ID'), max_length=20, unique=True)
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    profile_picture = models.FileField(upload_to='profile_pictures')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'department', 'university']

    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'







class Content(models.Model):
    course_name = models.CharField(max_length=100,default='',null=False) 
    course_code = models.CharField(max_length=100,default='',null=False) 
    contributor = models.CharField(max_length=100,default='',null=False) 
    image = models.CharField(max_length=100,default='',null=False) 
    description = models.CharField(max_length=300,default='',null=False)


class Content_Request(models.Model):
    course_name = models.CharField(max_length=100,default='',null=False) 
    course_code = models.CharField(max_length=100,default='',null=False) 
    semester = models.CharField(max_length=100,default='',null=False) 
    description = models.CharField(max_length=300,default='',null=False)