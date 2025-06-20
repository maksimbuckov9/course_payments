from django import forms
from .models import Course
from .models import Student
from .models import  Payment
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
