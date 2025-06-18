# create_user.py
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_payments.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='user1').exists():
    User.objects.create_user(username='user1', password='test12345')
    print("Пользователь user1 создан.")
else:
    print("Пользователь уже существует.")
