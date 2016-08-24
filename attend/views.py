from django.shortcuts import render,get_object_or_404
from .models import Class,Student
from django.contrib.auth.models import User
from .forms import ClassForm,StudentForm,ContactForm
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
    logout(request)
    return render(request,'attend/index.html',{'message':'You have been logged out Succcessfully!! Login in Bellow..'})

@csrf_protect
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password=request.POST['pwd1']
        email=request.POST['email']
        user=User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
        user.save()
        return render(request,'attend/reg_success.html')
    return render(request,'attend/register2.html')

@csrf_protect
def changepassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            username=request.user.username
            email=request.POST['email']
            password=request.POST['pwd1']
            user=User.objects.get(username=username)
            if user.email==email:
                user.set_password(password)
                user.save()
                return render(request,'attend/home.html',{'username':request.user.username,'error_message':'Password changed successfully'})
            else:
                return render(request,'attend/change_password2.html',{'username':request.user.username,'error_message':'Invalid E-Mail Address'})
        return render(request,'attend/change_password2.html',{'username':request.user.username})
        

def home(request):
    if not request.user.is_authenticated():
        return render(request,'attend/index.html')
    else:
        user=request.user
        username=user.username
        return render(request,'attend/home.html',{'username':username})

@csrf_protect
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

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
            sender=form.cleaned_data['sender']
            send_mail('Feedback from your site: %s'%subject,message,sender,['shubhankergoyal@gmail.com'],fail_silently=False)
            return render(request,'attend/thanks.html')
    return render(request,'attend/contact.html', {'form': form})




















