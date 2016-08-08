from django.shortcuts import render,get_object_or_404
from .models import Class,Student
from django.contrib.auth.models import User
from .forms import ClassForm,StudentForm,UserForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail

@csrf_protect
def index(request):
    if request.method=='POST':
        username=request.POST['Username']
        password =request.POST['Password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/home')
            else:
                return render(request,'attend/index.html',{'error_message':'Your account has been disabled'})
        else:
            return render(request,'attend/index.html',{'error_message':'Invalid Login'})
    return render(request,'attend/index.html')

def logout_user(request):
    form=UserForm(request.POST or None)
    logout(request)
    return render(request,'attend/index.html',{'form':form})

@csrf_protect
def register(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=User.objects.create_user(username=username,password=password,email=email)
            return render(request,'attend/reg_success.html')
    else:
        form=UserForm()
    return render(request,'attend/register.html',{'form':form})

def home(request):
    if not request.user.is_authenticated():
        return render(request,'attend/index.html')
    else:
        user=request.user
        username=user.username
        return render(request,'attend/home.html',{'username':username})

def create_class(request):
    if not request.user.is_authenticated():
        return render(request,'attend/index.html')
    else:
        if request.method=='POST':
            form=ClassForm(request.POST)
            if form.is_valid():
                clas=form.save(commit=False)
                clas.faculty=request.user
                clas.save()
                return render(request,'attend/detail.html',{'username':request.user.username,'clas':clas,'success_messsage':'Class Added Successfully'})
        else:
            form=ClassForm()
        return render(request,'attend/create_class.html',{'form':form,'username':request.user.username})

def create_student(request,clas_id):
    form=StudentForm(request.POST or None)
    clas = get_object_or_404(Class, pk=clas_id)
    if form.is_valid():
        clas_students=clas.student_set.all()
        for s in clas_students:
            if s.univ_roll_no==form.cleaned_data.get("univ_roll_no"):
                return render(request,'attend/create_student.html',{'clas':clas,'username':request.user.username,'form':form,'error_message':'You already added this Student'})
        student=form.save(commit=False)
        student.sclass=clas
        student.save()
        return render(request,'attend/detail.html',{'clas':clas,'username':request.user.username})
    return render(request,'attend/create_student.html',{'clas':clas,'form':form,'username':request.user.username})

def class_list(request):
    list=Class.objects.filter(faculty=request.user)
    return render(request,'attend/class_list.html',{'list':list,'username':request.user.username})

def student_list(request,clas_id):
    clas=get_object_or_404(Class, pk=clas_id)
    return render(request,'attend/student_list.html',{'clas':clas,'username':request.user.username})

def mark_class_list(request):
    list=Class.objects.filter(faculty=request.user)
    return render(request,'attend/mark_class_list.html',{'list':list,'username':request.user.username})

def mark_attendence(request,clas_id):
    if not request.user.is_authenticated():
        return render(request,'attend/index.html')
    else:
        clas=get_object_or_404(Class, pk=clas_id)
        if request.method=='POST':
            attendList=request.POST.getlist('list')
            for stud in clas.student_set.all():
                for i in attendList:
                    if stud.name==i:
                        stud.count=stud.count+1
                stud.total=stud.total+1
                stud.save()
            return render(request,'attend/attend_success.html',{'clas':clas,'username':request.user.username})
        return render(request,'attend/mark_attendence.html',{'clas':clas,'username':request.user.username})





















