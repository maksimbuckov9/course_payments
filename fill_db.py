import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from payments.models import Course, Student, Payment  # Замените payments на имя вашего приложения

# Данные для заполнения
course_names = [
    "Программирование на Python", "Веб-разработка", "Анализ данных", "Машинное обучение",
    "Дизайн интерфейсов", "Управление проектами", "Основы бухгалтерии", "Маркетинг",
    "Английский язык", "Фотография", "Музыка", "Иностранные языки",
    "Йога и фитнес", "Психология", "Кулинария", "Технический английский",
    "3D-моделирование", "Финансы", "Логистика", "Электроника"
]

teacher_names = [
    "Иван Иванов", "Петр Петров", "Сергей Сергеев", "Анна Смирнова",
    "Ольга Кузнецова", "Дмитрий Васильев", "Мария Попова", "Елена Соколова",
    "Алексей Морозов", "Наталья Ковалёва"
]

student_names = [
    "Алексей", "Мария", "Иван", "Ольга", "Дмитрий", "Елена", "Сергей", "Наталья",
    "Павел", "Татьяна", "Виктор", "Анна", "Кирилл", "Ирина", "Максим", "Юлия",
    "Роман", "Светлана", "Евгений", "Людмила"
]

statuses = ['paid', 'pending']

# Создаем 20 курсов
courses = []
for i in range(20):
    start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
    end_date = start_date + timedelta(days=random.randint(30, 90))
    course = Course.objects.create(
        name=course_names[i],
        description=f"Описание курса '{course_names[i]}'",
        teacher=random.choice(teacher_names),
        price=random.choice([10000.00, 15000.00, 20000.00]),
        start_date=start_date,
        end_date=end_date
    )
    courses.append(course)

# Создаем 20 пользователей и студентов
students = []
for i in range(20):
    username = f'user{i+1}'
    user = User.objects.create_user(
        username=username,
        password='password123',
        first_name=student_names[i],
        last_name=f"Фамилия{i+1}"
    )
    student = Student.objects.create(
        user=user,
        passport=f"1234 {random.randint(100000, 999999)}",
        phone=f"+7{random.randint(9000000000, 9999999999)}",
        name=f"{student_names[i]} Фамилия{i+1}"
    )
    students.append(student)

# Создаем 20 оплат
for i in range(20):
    student = random.choice(students)
    course = random.choice(courses)
    Payment.objects.create(
        student=student,
        course=course,
        amount=course.price,
        status=random.choice(statuses)
    )

print("База успешно наполнена!")
