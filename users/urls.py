from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('users/register/', views.register_view, name='register'),
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout_view, name='logout'),
]