"""multi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import( TeacherSignupView, StudentSignupView,
                             UserLoginView, StudentOnlyView, TeacherOnlyView, 
                             AdminSignupView, AdminOnlyView,
                             AdminAddStudent, AdminAddTeacher, TeacherAddStudent,
                             UserPasswordResetView, SendPasswordResetEmailView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/signup/', AdminSignupView.as_view()),
    path('api/teacher/signup/', TeacherSignupView.as_view()),
    path('api/student/signup/', StudentSignupView.as_view()),
    path('api/login/', UserLoginView.as_view()),
    path('api/admin/dashboard/', AdminOnlyView.as_view()),
    path('api/teacher/dashboard/', TeacherOnlyView.as_view()),
    path('api/student/dashboard/', StudentOnlyView.as_view()),
    path('api/admin/add-teacher/', AdminAddTeacher.as_view()),
    path('api/admin/add-student/', AdminAddStudent.as_view()),
    path('api/teacher/add-student/', TeacherAddStudent.as_view()),
    path('api/send-reset-password-email/', SendPasswordResetEmailView.as_view()),
    path('api/reset-password/<uid>/<token>/', UserPasswordResetView.as_view()),
]
