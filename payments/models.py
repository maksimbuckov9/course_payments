from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passport = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
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