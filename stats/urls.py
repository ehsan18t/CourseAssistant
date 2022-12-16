from django.urls import path

from . import views

urlpatterns = [
    path('', views.stats, name="stats"),
    path('semester=<int:pk>', views.courses, name="courses"),
    path('semester=<int:s_pk>&course=<int:c_pk>', views.assessments, name="assessments"),
]
