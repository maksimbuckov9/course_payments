#!/usr/bin/python3

import django
import random
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_payments.settings')
django.setup()

from django.db.models import Count
from payments.models import CustomUser, Student

# -----------------------------
# 1. Исправляем дубли username
# -----------------------------
duplicates = CustomUser.objects.values('username')\
    .annotate(count=Count('username'))\
    .filter(count__gt=1)

for dup in duplicates:
    users = list(CustomUser.objects.filter(username=dup['username']))
    # оставляем первого пользователя, остальных исправляем
    for user in users[1:]:
        new_username = f"{user.username}_{random.randint(1000, 9999)}"
        print(f"Изменяем {user.username} -> {new_username}")
        user.username = new_username
        user.save()

print("Дубли username исправлены.")

# -----------------------------
# 2. Очистка таблицы Student
# -----------------------------
Student.objects.all().delete()
print("Таблица Student очищена.")

# -----------------------------
# 3. Данные для генерации
# -----------------------------
first_names = [
    "Алексей", "Мария", "Иван", "Ольга", "Дмитрий", "Елена", "Сергей", "Наталья",
    "Павел", "Татьяна", "Виктор", "Анна", "Кирилл", "Ирина", "Максим", "Юлия",
    "Роман", "Светлана", "Евгений", "Людмила"
]

last_names = [
    "Иванов", "Петров", "Сидоров", "Смирнова", "Кузнецова", "Васильев", "Попова",
    "Соколова", "Морозов", "Ковалёв", "Новиков", "Фёдоров", "Михайлова",
    "Александров", "Григорьев", "Тарасов", "Воронова", "Зайцев", "Орлов", "Кириллов"
]

used_passports = set()
used_phones = set()

# -----------------------------
# 4. Создаём студентов
# -----------------------------
student_users = CustomUser.objects.filter(role='student')
created_count = 0

for user in student_users:
    if hasattr(user, 'student'):
        continue  # студент уже есть, пропускаем

    first_name = user.first_name or random.choice(first_names)
    last_name = user.last_name or random.choice(last_names)
    full_name = f"{first_name} {last_name}"

    # Генерируем уникальный паспорт
    while True:
        passport = f"1234 {random.randint(100000, 999999)}"
        if passport not in used_passports:
            used_passports.add(passport)
            break

    # Генерируем уникальный телефон
    while True:
        phone = f"+7{random.randint(9000000000, 9999999999)}"
        if phone not in used_phones:
            used_phones.add(phone)
            break
    user.save()

    Student.objects.create(
        user=user,
        name=full_name,
        passport=passport,
        phone=phone
    )
    created_count += 1

print(f"{created_count} студентов успешно созданы!")
