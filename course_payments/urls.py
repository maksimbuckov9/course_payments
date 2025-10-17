from django.contrib import admin
from django.urls import path, include
from payments import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("", lambda request: redirect("login")),  # редирект с / на страницу логина
    path("payments/", include("payments.urls")), # пути приложения

    # Подключаем стандартные пути для login/logout
    path('accounts/', include('django.contrib.auth.urls')),

    # Настройка LogoutView с использованием своего шаблона
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Другие пути вашего приложения
    path('', include('payments.urls')),
]