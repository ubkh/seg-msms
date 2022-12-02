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


schoolurlpatterns = [

    path('', views.school_home, name='school_home'),  # school_home

    # Student
    path('lesson/request', views.request_lesson, name='request_lesson'),
    path('lesson/<hashid:pk>/modify/', views.modify_lesson, name='modify_lesson'),

    path('lesson/<hashid:pk>/invoice/', views.booking_invoice, name='booking_invoice'),

    # Teacher

    # Administrator

    path('student/<hashid:pk>/bookings/', views.open_bookings, name='open_bookings'),
    path('student/<hashid:pk>/bookings/fulfill', views.fulfill_lesson, name='fulfill_lesson'),

    path('transfers/', views.TransferListView.as_view(), name='transfers'),
    path('transfers/create/', views.TransferCreateView.as_view(), name='create_transfer'),

    path('terms/', views.view_terms, name='terms'),
    path('term/<int:pk>/edit', views.edit_term, name='edit_term'),

    # Super-administrator

    path('administrators/', views.AdministratorListView.as_view(), name='administrators'),
    path('administrators/create/', views.AdministratorCreateView.as_view(), name='create_administrator'),
    path('administrators/<hashid:pk>/modify/', views.AdministratorUpdateView.as_view(), name='modify_administrator'),

    # Director
    # path(modify_school)


]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('log_out/', views.log_out, name='log_out'),
    path('home/', views.home, name='home'),  # school_home
    # path('', include(schoolurlpatterns)), DELETE
    path('school/<int:school>/', include(schoolurlpatterns)),


    # Student
    path('school/', views.SchoolListView.as_view(), name='list_school'),

    # Adult-student

    path('children/', views.ChildListView.as_view(), name='children'),
    path('children/create/', views.ChildCreateView.as_view(), name='create_child'),

    # Director
    path('school/create/', views.SchoolCreateView.as_view(), name='create_school')

    # System-administrator

]
