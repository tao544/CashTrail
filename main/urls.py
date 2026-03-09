from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('child-login/', views.child_login, name='child_login'),
    path('transactions/', views.all_transactions, name='all_transactions'),
    path('mychildren/', views.mychildren, name='mychildren'),
    path('Addchild/', views.Addchild, name='Addchild'),
    path( "child/<int:child_id>/", views.child_detail, name="child_detail"),
    path('childrendashboard/', views.childrendashboard, name='childrendashboard'),
    path("Addexpense/", views.Addexpense, name="Addexpense"),
    path("Mytransactions/", views.Mytransactions, name="Mytransactions"),
    path("Childprofile", views.Childprofile, name="Childprofile"),
    path("Fundwallet/", views.Fundwallet, name="Fundwallet"),

    ]