from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
        ('student', 'Студент'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    passport = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Оплачено'),
        ('pending', 'Ожидается'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} — {self.course} — {self.amount} руб. — {self.get_status_display()}"
