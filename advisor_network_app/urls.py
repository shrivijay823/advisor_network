from django.urls import path

from . import views
from django.contrib import admin
app_name='advisor_network_app'
urlpatterns=[
    path('',views.index.as_view(),name='user'),
    path('user/<int:id>/advisor',views.index.advview,name='advview'),
    path('user/<int:uid>/advisor/<int:aid>',views.index.bookcall,name='bookcall'),
    path('user/<int:uid>/advisor/booking/',views.index.allbooks,name='allbooks'),
    path('user/<str:auth>/',views.signinupview.as_view(),name='signupin'),
    path('admin/login',views.adminview.as_view(),name='adminlogin'),
    path('admin/logout',views.adminview.logout,name='adminlogout'),
    path('admin',views.adminview.adminpage,name='adminview'),
    path('admin/add advisor',views.index.addadv,name='addadv')
]
