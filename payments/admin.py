from django.contrib import admin
from .models import Course

admin.site.register(Course)
from .models import Student
admin.site.register(Student)