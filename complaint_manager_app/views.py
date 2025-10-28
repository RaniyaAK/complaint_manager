from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm,LoginForm
from .models import Complaint

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render
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

@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        complaints = Complaint.objects.all().order_by('-created_at')
        return render(request, 'admin_dashboard.html', {
            'username': request.user.username,
            'mycomplaints': complaints
        })
    else:
        return redirect('user_dashboard')

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
def all_complaints(request):
    mycomplaints = Complaint.objects.all()  # all complaints for admin
    return render(request, 'all_complaints.html', {'mycomplaints': mycomplaints})


# user
@login_required(login_url='login')
def success(request):
    return render(request, 'success.html', {"username": request.user.username})



@csrf_exempt
@login_required
def update_status(request, complaint_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.status = new_status
            complaint.save()  # This will automatically update `updated_at`

            return JsonResponse({
                "success": True,
                "new_status": complaint.status,
                "updated_at": complaint.updated_at.strftime("%b %d, %Y %H:%M"),
            })
        except Complaint.DoesNotExist:
            return JsonResponse({"success": False, "error": "Complaint not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
def complaints_list(request):
    # Fetch all complaints (only subject & description shown)
    complaints = Complaint.objects.all().order_by('-id')  # latest first

    # Pagination setup (5 complaints per page)
    paginator = Paginator(complaints, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'complaints_list.html', {'page_obj': page_obj})
