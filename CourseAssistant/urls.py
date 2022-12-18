from django.contrib import admin
from django.urls import path, include
from base.views import install_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('stats/', include('stats.urls')),
    path('install/',  install_page),
]
