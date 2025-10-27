from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm,LoginForm,UpdateForm
from .models import Complaint


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already registered'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'registration.html')


def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
              auth_login(request, user)
              if user.is_superuser:
                return redirect('admin_dashboard')
              else:
                return redirect('user_dashboard')
            else:
                error_message = 'Invalid username or password'
        else:
                error_message = 'Invalid username or password'        
    else:
        form = LoginForm()
    return render(request, 'login.html',{'form':form, 'error_message':error_message})


# passwords
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            return redirect('reset_password', email=user.email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
    return render(request, 'forgot_password.html')


def reset_password(request, email):
    success = False  

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                success = True
                messages.success(request, 'Password reset successful! You can now log in.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid user.')

    return render(request, 'reset_password.html', {'email': email, 'success': success})


# logout
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# admin
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {"username": request.user.username})


@login_required(login_url='login')
def all_complaints(request):
    return render(request, 'all_complaints.html', {"username": request.user.username})


# user
@login_required(login_url='login')
def user_dashboard(request):
    return render(request, 'user_dashboard.html', {"username": request.user.username})



@login_required
def complaint_registration_form(request):
    message = None  

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit = False)
            complaint.user = request.user
            complaint.save()
            return redirect('success')

    else:
        form = ComplaintForm()

    return render(request, 'complaint_registration_form.html', {
        'form': form,
        'message': message
    })

@login_required
def submitted_complaints(request):
    mycomplaints = Complaint.objects.filter(user=request.user)
    return render(request, 'submitted_complaints.html', {"mycomplaints": mycomplaints})


@login_required

def update_complaint(request,id):
    complaint = get_object_or_404(Complaint , id=id, user=request.user)
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=complaint)
        if form.is_valid():
            form.save()
            print("Updated")
        else:
            print(form.errors)
        return redirect('submitted_complaints')
    else:
        form = UpdateForm(instance=complaint)
    return render(request, 'update_complaint.html', {'username': request.user.username,'complaint': complaint,'form':form })


# user
@login_required(login_url='login')
def success(request):
    return render(request, 'success.html', {"username": request.user.username})

