from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
