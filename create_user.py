# create_user.py
import django
import os
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_payments.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

args = sys.argv

if len(args) == 4:
    User = get_user_model()
    if not User.objects.filter(username=args[1]).exists() and args[3] in ['student', 'manager', 'admin']:
        user = User.objects.create_user(username=args[1], password=args[2])
        user.role = args[3]
        user.save()
        print("Пользователь создан.")
    else:
        print("Error.")

else:
    print('Syntax: create_user.py <name> <password> <role: admin/manager/student>')

