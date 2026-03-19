from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path('child-login/', views.child_login, name='child_login'),

    path('transactions/', views.Mytransactions, name='Mytransactions'),

    path('mychildren/', views.mychildren, name='mychildren'),

    path('Addchild/', views.Addchild, name='Addchild'),

    # ✅ KEEP ONLY THIS ONE
    path('reset-child-password/<int:child_id>/', views.reset_child_password, name='reset_child_password'),

    path("child/<int:child_id>/", views.child_detail, name="child_detail"),

    path('childrendashboard/', views.childrendashboard, name='childrendashboard'),

    path('child-dashboard/<int:child_id>/', views.childrendashboard, name='view_child_dashboard'),

    path("Addexpense/", views.Addexpense, name="Addexpense"),

    path("Childprofile/", views.Childprofile, name="Childprofile"),

    path("Fundwallet/", views.Fundwallet, name="Fundwallet"),
]