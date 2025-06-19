from django import forms
from .models import Course
from .models import Student
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'