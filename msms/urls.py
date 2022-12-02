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
from django.urls import path, register_converter
from lessons import views
from msms.hash import HashIDConverter

register_converter(HashIDConverter, "hashid")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('log_out/', views.log_out, name='log_out'),
    path('home/', views.home, name='home'),
    path('lesson/request', views.request_lesson, name='request_lesson'),
    path('lesson/<hashid:pk>/modify/', views.modify_lesson, name='modify_lesson'),
    path('student/<hashid:pk>/bookings/', views.open_bookings, name='open_bookings'),
    path('student/<hashid:pk>/bookings/fulfill', views.fulfill_lesson, name='fulfill_lesson'),
    path('lesson/<hashid:pk>/invoice/', views.booking_invoice, name='booking_invoice'),
    path('administrators/', views.AdministratorListView.as_view(), name='administrators'),
    path('administrators/create/', views.AdministratorCreateView.as_view(), name='create_administrator'),
    path('administrators/<hashid:pk>/modify/', views.AdministratorUpdateView.as_view(), name='modify_administrator'),
    path('transfers/', views.TransferListView.as_view(), name='transfers'),
    path('transfers/create/', views.TransferCreateView.as_view(), name='create_transfer'),
    path('children/', views.ChildListView.as_view(), name='children'),
    path('children/create/', views.ChildCreateView.as_view(), name='create_child'),
    path('terms/', views.view_terms, name='terms'),
    path('term/<int:pk>/edit', views.edit_term, name='edit_term'),
    path('student/<hashid:pk>/ban_client/', views.ban_client, name='ban_client')
]
