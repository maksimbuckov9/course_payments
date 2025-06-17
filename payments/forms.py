from django import forms
from .models import Payment, Course, Student

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['course', 'amount', 'status']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['passport', 'phone']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'price', 'start_date', 'end_date']
