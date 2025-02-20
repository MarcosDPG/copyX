# users/forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_name', 'email', 'name', 'birth_date', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Encripta la contraseña
        if commit:
            user.save()
        return user