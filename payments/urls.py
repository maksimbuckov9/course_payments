from django.urls import path
from . import views

urlpatterns = [
    # ====== Курсы ======
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # ====== Пользователи ======
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),

    # ====== Студенты ======
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # ====== Оплаты ======
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('payments/<int:payment_id>/contract/', views.generate_contract, name='generate_contract'),
    path('export_payments_excel/', views.export_payments_excel, name='export_payments_excel'),
    path('payments_stats/', views.payments_stats, name='payments_stats'),
]
