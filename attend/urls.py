from django.conf.urls import url
from . import views

app_name='attend'

urlpatterns=[
    url(r'^$',views.index, name='index'),
    url(r'^login/$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^home/$',views.home,name='home'),
    url(r'^logout/$',views.logout_user,name='logout'),
    url(r'^add_class/$',views.create_class,name='create_class'),
    url(r'^(?P<clas_id>[0-9]+)/add_student/$',views.create_student,name='create_student'),
    url(r'^class_list/$',views.class_list,name='class_list'),
    url(r'^(?P<clas_id>[0-9]+)/student_list/$',views.student_list,name='student_list'),
    url(r'^mark_class_list/$',views.mark_class_list,name='mark_class_list'),
    url(r'^(?P<clas_id>[0-9]+)/mark_attendence/$',views.mark_attendence,name='mark_attendence'),
    url(r'^contact/$',views.contact,name='contact')
]