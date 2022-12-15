from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, s_id, first_name, last_name, passwords, department, university, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, s_id, first_name, last_name, passwords, department, university, **other_fields)

    def create_user(self, email, s_id, first_name, last_name, passwords, department, university, **other_fields):
        # Validations
        if not email:
            raise ValueError(_('You must provide an email address'))
        if university.validate_email(email) is False:
            raise ValueError(_('You must provide a valid email address'))
        if not s_id:
            raise ValueError(_('You must provide a student ID'))
        if university.validate_sid(s_id) is False:
            raise ValueError(_('You must provide a valid student ID'))

        # Normalizations and creation 
        email = self.normalize_email(email)
        user = self.model(email=email, s_id=s_id, first_name=first_name, last_name=last_name, passwords=passwords,
                          department=department, university=university, **other_fields)
        user.save()
        return user


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    email_pattern = models.CharField(max_length=100)  # university pattern
    sid_pattern = models.CharField(max_length=100)  # student id pattern

    def __str__(self):
        return f'{self.name} {self.domain} ({self.email_pattern}) - {self.sid_pattern}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.university})'


# Create user extending default user model
class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    s_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_('email address'), max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passwords = models.CharField(max_length=300)
    profile_picture = models.FileField(upload_to='profile_pictures')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 's_id'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'passwords', 'department', 'university']
    
    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

