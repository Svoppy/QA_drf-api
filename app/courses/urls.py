from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll, name='enroll'),
    path('<int:pk>/drop/', views.drop_course, name='drop_course'),
    path('my/', views.my_courses, name='my_courses'),
]
