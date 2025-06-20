from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm
from .models import Student
from .forms import StudentForm
from .forms import PaymentForm
import os
from django.conf import settings
from datetime import datetime
from docx import Document
from .models import Payment  # предположим, что Payment у вас импортирован здесь
import openpyxl
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.db.models import Q

@login_required
def payment_list(request):
    payments = Payment.objects.select_related('student__user', 'course')

    query = request.GET.get('q', '')
    course_id = request.GET.get('course', '')
    status = request.GET.get('status', '')

    if query:
        payments = payments.filter(
            Q(student__user__first_name__icontains=query) |
            Q(student__user__last_name__icontains=query)
        )
    if course_id:
        payments = payments.filter(course_id=course_id)
    if status:
        payments = payments.filter(status=status)

    courses = Course.objects.all()

    context = {
        'payments': payments,
        'courses': courses,
        'query': query,
        'selected_course': course_id,
        'selected_status': status,
    }
    return render(request, 'payments/payment_list.html', context)

@login_required
def payments_stats(request):
    # Сумма оплат по курсам
    course_payments = (
        Payment.objects.values('course__name')
        .annotate(total=Sum('amount'))
    )
    course_labels = [item['course__name'] for item in course_payments]
    course_values = [item['total'] for item in course_payments]

    # Количество оплат по месяцам (с TruncMonth)
    monthly = (
        Payment.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    month_labels = [item['month'].strftime('%Y-%m') for item in monthly]
    month_values = [item['count'] for item in monthly]

    context = {
        'course_labels': course_labels,
        'course_values': course_values,
        'month_labels': month_labels,
        'month_values': month_values,
    }
    return render(request, 'payments/payments_stats.html', context)
def export_payments_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Оплаты"

    # Заголовки
    ws.append(['Студент', 'Курс', 'Сумма', 'Дата'])

    # Данные
    for payment in Payment.objects.select_related('student__user', 'course'):
        ws.append([
            payment.student.user.get_full_name(),
            payment.course.name,
            payment.amount,
            payment.date.strftime('%d.%m.%Y')
        ])

    # Ответ
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=payments.xlsx'
    wb.save(response)
    return response

@login_required 
def generate_contract(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    # Абсолютный путь к шаблону
    template_path = os.path.join(settings.BASE_DIR, 'static', 'contracts', 'contract_template.docx')
    
    doc = Document(template_path)

    # Замена плейсхолдеров
    for p in doc.paragraphs:
        p.text = p.text.replace('{{ contract_number }}', str(payment.id))
        p.text = p.text.replace('{{ date }}', datetime.now().strftime('%d.%m.%Y'))
        p.text = p.text.replace('{{ student_name }}', payment.student.user.get_full_name())
        p.text = p.text.replace('{{ course_name }}', payment.course.name)
        p.text = p.text.replace('{{ start_date }}', payment.course.start_date.strftime('%d.%m.%Y'))
        p.text = p.text.replace('{{ end_date }}', payment.course.end_date.strftime('%d.%m.%Y'))
        p.text = p.text.replace('{{ price }}', str(payment.amount))

    # Ответ как файл
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    filename = f"contract_{payment.student.user.username}_{payment.course.name}.docx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    doc.save(response)
    return response



@login_required
def dashboard(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    return render(request, 'payments/dashboard.html', {
        'courses': courses,
        'students': students
    })

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
    
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'payments/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'payments/student_form.html', {'form': form, 'title': 'Добавить студента'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'payments/student_form.html', {'form': form, 'title': 'Редактировать студента'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'payments/student_confirm_delete.html', {'student': student})
    



@login_required
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Добавить оплату'})

@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Редактировать оплату'})

@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')
    return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})
