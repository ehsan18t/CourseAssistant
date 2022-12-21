from django.contrib import admin

from .models import Department
from .models import University
from .models import User
from .models import Content, Content_Request

# Register your models here.
admin.site.register(User)
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Content)
admin.site.register(Content_Request)
