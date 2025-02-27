from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    user = request.user
    if user == 'AnonymousUser':
        return redirect('/users/register/')
    else:
        return redirect('/users/login/')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation_password = request.POST.get('confirmation_password')
        email = request.POST.get('email')

        if password == confirmation_password:
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
        else:
            messages.info(request, "Confirmation password and password do not match")

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation_password = request.POST.get('confirmation_password')

        if password == confirmation_password:
            if not User.objects.filter(username = username).exists():
                messages.error(request, "Invalid Username")
                return redirect("/users/login/")

            site_user = authenticate(username = username, password = password)

            if site_user is None:
                messages.error(request, "Invlaid Password")
                return redirect('/users/login/')
            else:
                auth_login(request, site_user)
                return redirect('/stationery_items/')
        else:
            messages.info(request, "Confirmation password and password do not match")

    return render(request, 'users/login.html')


@login_required(login_url="/users/login/")
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('/')