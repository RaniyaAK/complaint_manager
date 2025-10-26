from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Password confirmation check
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already registered'})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
               return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {"username": request.user.username})

@login_required(login_url='login')
def user_dashboard(request):
    return render(request, 'user_dashboard.html', {"username": request.user.username})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')