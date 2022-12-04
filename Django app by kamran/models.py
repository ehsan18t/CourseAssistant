from django.db import models


# Create your models here.

class person:
    name : str
    code : int
    show : bool

class content(models.Model):
    course_name = models.CharField(max_length=100,default='',null=False) 
    course_code = models.CharField(max_length=100,default='',null=False) 
    contributor = models.CharField(max_length=100,default='',null=False) 
    image = models.CharField(max_length=100,default='',null=False) 
    comment = models.CharField(max_length=1000,default='',null=False)


class details(models.Model):
    type= models.CharField(max_length=100,default='',null=False)   
    name= models.CharField(max_length=100,default='',null=False)   

