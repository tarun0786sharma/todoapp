from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete"),
    path('logout/', views.logout, name='logout'),
]