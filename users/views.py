from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'users/index.html')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        queryset = User.objects.filter(username = username)

        if queryset.exists():
            messages.info(request, "Username Already Taken")
            return redirect("/users/register/")
        else:
            user = User.objects.create(first_name = first_name, last_name = last_name, username = username, email = email)
            user.set_password(password)
            user.save()
            messages.info(request, "Account created successfully")
            return redirect('/users/login/')

    return render(request, 'users/register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect("/users/login/")
        
        site_user = authenticate(username = username, password = password)

        if site_user is None:
            messages.error(request, "Invlaid Password")
            return redirect('/users/login/')
        else:
            login(request, site_user)
            return redirect('/goods/')
        
    return render(request, 'users/login.html')
            

def logout_page(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('/')