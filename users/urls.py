from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="users_home"),
    path('register/', register_page, name="register-page"),
    path('login/', login_page, name="login-page"),
    path('logout/', logout_page, name="logout-page"),
]