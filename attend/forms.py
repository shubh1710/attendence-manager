from django import forms
from .models import Class,Student,Contact
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


class ContactForm(ModelForm):
    message=forms.CharField(widget=forms.Textarea)
    class Meta:
        model=Contact
        fields=['subject','message','sender']

