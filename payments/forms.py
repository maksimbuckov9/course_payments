from django import forms
from .models import Course
from .models import Student
from .models import  Payment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'



class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)  # явно поле role

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  # забираем роль из формы
        if commit:
            user.save()
        return user
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'role')