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
from unicodedata import name
from django.contrib import admin
from django.urls import path, register_converter, include
from lessons import views
from msms.hash import HashIDConverter

register_converter(HashIDConverter, "hashid")


school_urlpatterns = [
    path('', views.SchoolHomeView.as_view(), name='school_home'),
    path('manage/', views.SchoolManageView.as_view(), name='manage'),

    # Client
    path('lesson/request', views.LessonRequestView.as_view(), name='request_lesson'),
    path('lesson/<hashid:pk>/modify/', views.LessonModifyView.as_view(), name='modify_lesson'),

    path('lesson/<hashid:pk>/invoice/', views.BookingInvoiceView.as_view(), name='booking_invoice'),

    # Teacher
    # path()

    # Administrator
    path('student/<hashid:pk>/bookings/', views.BookingListView.as_view(), name='open_bookings'),
    path('student/<hashid:pk>/bookings/fulfill', views.LessonFulfillView.as_view(), name='fulfill_lesson'),

    path('transfers/', views.TransferListView.as_view(), name='transfers'),
    path('transfers/create/', views.TransferCreateView.as_view(), name='create_transfer'),

    # Super-administrator
    path('users/', views.SchoolUserListView.as_view(), name='users'),
    path('administrators/', views.AdministratorListView.as_view(), name='administrators'),
    path('administrators/create/', views.AdministratorCreateView.as_view(), name='create_administrator'),
    path('administrators/<hashid:pk>/modify/', views.AdministratorUpdateView.as_view(), name='modify_administrator'),

    # Director
    path('student/<hashid:pk>/ban_client/', views.BanClientView.as_view(), name='ban_client')
    # path(name='modify_school')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('school/<int:school>/', include(school_urlpatterns)),

    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('log_out/', views.log_out, name='log_out'),

    # Adult-user
    path('children/', views.ChildListView.as_view(), name='children'),
    path('children/create/', views.ChildCreateView.as_view(), name='create_child'),

    # Director
    path('school/create/', views.SchoolCreateView.as_view(), name='create_school'),

    # System-administrator
    # path(name='create_director')

    # Administrator (Move inside school?)
    path('terms/', views.view_terms, name='terms'),
    path('term/<int:pk>/edit', views.edit_term, name='edit_term'),

]
