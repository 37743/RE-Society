from django.contrib import admin 
from django.urls import path, include
from . import views


urlpatterns = [
    path('' ,views.home , name = 'home'),
    path('login/' , views.signIn , name = 'signIn'),
    path('signup/' , views.signUp , name = 'signup'),
    path('logout/' , views.signOut , name = 'signout'),
    path('workers/', views.WorkerListView.as_view(), name='worker_list'),
    path('detailed/<int:pk>/', views.WorkerDetailsView.as_view(), name='worker_detail'),
]