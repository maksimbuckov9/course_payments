from django.shortcuts import render, redirect
from .models import Student, Course, Payment, Contract
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    students_count = Student.objects.count()
    courses_count = Course.objects.count()
    payments_count = Payment.objects.filter(status='paid').count()
    context = {
        'students_count': students_count,
        'courses_count': courses_count,
        'payments_count': payments_count,
    }
    return render(request, 'payments/dashboard.html', context)

@login_required
def students_list(request):
    students = Student.objects.all()
    return render(request, 'payments/students_list.html', {'students': students})
