from django import forms
from .models import Class,Student
from django.contrib.auth.models import User
from django.forms import ModelForm

class ClassForm(ModelForm):
    class Meta:
        model=Class
        fields='__all__'

class StudentForm(ModelForm):
    class Meta:
        model=Student
        fields='__all__'
        exclude=['sclass','createdAt','count','total']

class UserForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']
