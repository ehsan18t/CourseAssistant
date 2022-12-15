from django.contrib import admin
from .models import University
from .models import Department
from .models import User

# Register your models here.
admin.site.register(User)
admin.site.register(University)
admin.site.register(Department)
