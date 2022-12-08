"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, register_converter, include

from lessons import views
from msms.hash import HashIDConverter

register_converter(HashIDConverter, "hashid")

school_urlpatterns = [
    path('', views.SchoolHomeView.as_view(), name='school_home'),

    # Client
    path('lessons/', views.LessonListView.as_view(), name='client_lessons'),
    path('lesson/request/', views.LessonRequestView.as_view(), name='request_lesson'),
    path('lesson/<hashid:pk>/modify/', views.LessonModifyView.as_view(), name='modify_lesson'),
    path('lesson/<hashid:pk>/invoice/', views.LessonInvoiceView.as_view(), name='booking_invoice'),

    path('transactions/', views.TransactionsListView.as_view(), name='client_transactions'),

    path('timetable/', views.TimetableView.as_view(), name='timetable'),

    # Teacher
    path('teacher/timetable/', views.TeacherTimetableView.as_view(), name='teacher_timetable'),

    # Administrator
    path('bookings/', views.BookingListView.as_view(), name='school_bookings'),
    path('lesson/<hashid:pk>/fulfill/', views.LessonFulfillView.as_view(), name='fulfill_lesson'),

    path('transfers/', views.SchoolTransferListView.as_view(), name='school_transfers'),
    path('transfer/create/', views.TransferCreateView.as_view(), name='create_transfer'),

    path('terms/', views.TermsView.as_view(), name='terms'),
    path('term/<int:pk>/edit/', views.TermEditView.as_view(), name='edit_term'),

    # Super-administrator
    path('members/', views.SchoolUserListView.as_view(), name='members'),
    path('member/<hashid:pk>/manage/', views.ManageStudentView.as_view(), name='manage_member'),

    # Director
    path('manage/', views.SchoolManageView.as_view(), name='manage_school')
]

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('home/', views.HomeView.as_view(), name='home'),
    path('school/<int:school>/', include(school_urlpatterns)),

    path('register/', views.register_view, name='register'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/<hashid:pk>/edit/', views.EditUserView.as_view(), name='edit_profile'),
    path('profile/<hashid:pk>/password_change/', views.ChangePasswordView.as_view(), name='password_change'),

    # Adult-user
    path('children/', views.ChildListView.as_view(), name='children'),
    path('children/create/', views.ChildCreateView.as_view(), name='create_child'),

    # Director
    path('school/create/', views.SchoolCreateView.as_view(), name='create_school'),

    # System-administrator
    path('director/create/', views.DirectorCreateView.as_view(), name='create_director')
]
