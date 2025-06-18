from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

@login_required
def dashboard(request):
    return render(request, 'payments/dashboard.html')

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'payments/courses_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'payments/course_form.html', {'form': form, 'title': 'Добавить курс'})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'payments/course_form.html', {'form': form, 'title': 'Редактировать курс'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'payments/course_confirm_delete.html', {'course': course})
