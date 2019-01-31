from django.db import models
from django.contrib.auth.models import User
import datetime

BRANCH_CHOICES=(
    ('CSE','Computer Science and Engineering'),
    ('IT','Information Technology'),
    ('ME','Mechanical Engineering'),
    ('ECE','Electronics and Communication Engineering'),
    ('EE','Electrical Engineering'),
    ('EEE','Electrical and Electronics Engineering'),
    ('CE','Civil Engineering'),
    ('ICE','Instrumentation and Control Engineering'),
)

SEM_CHOICES=(
    ('I','I'),
    ('II','II'),
    ('III','III'),
    ('IV','IV'),
    ('V','V'),
    ('VI','VI'),
    ('VII','VII'),
    ('VIII','VIII'),
)

SEC_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
)
class Class(models.Model):
    branch=models.CharField(max_length=20,choices=BRANCH_CHOICES)
    semester=models.CharField(max_length=20,choices=SEM_CHOICES)
    section=models.CharField(max_length=5,choices=SEC_CHOICES)
    faculty=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=20)
    lastmarkedAt=models.CharField(max_length=100,null=True)
    def __str__(self):
        return ('%s-%s%s-%s' % (self.semester,self.branch,self.section,self.subject))

class Student(models.Model):
    name=models.CharField(max_length=20)
    add_no=models.CharField(max_length=10,null=True)
    univ_roll_no=models.CharField(max_length=10,null=True)
    email=models.EmailField(max_length=50)
    phoneno=models.CharField(max_length=15)
    sclass=models.ForeignKey(Class,on_delete=models.CASCADE)
    count=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Contact(models.Model):
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=200)
    sender=models.EmailField(max_length=50)






