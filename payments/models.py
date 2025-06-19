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
    def __str__(self):
        return self.name
