from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from user_dashboard.views import dashboard_user


# Create your views here.

def register_view(request):
        if request.user.is_authenticated:
               return redirect('user_dashboard:dashboard_user')
        if request.method == 'POST':
                form = UserProfileForm(request.POST)
                if form.is_valid():
                        first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
                        email = form.cleaned_data['email']
                        phone_number = form.cleaned_data['phone_number']
                        address = form.cleaned_data['address']
                        state = form.cleaned_data['state']
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        profile_picture = request.FILES['profile_picture']

                        # Check for existing record with the same email
                        if UserProfile.objects.filter(email=email).exists():
                                return render(request, 'register.html', {'duplicate_message': 'Email Exists. Use another.'})
                        elif UserProfile.objects.filter(phone_number = phone_number):
                                return render(request, 'register.html', {'duplicate_message': 'Phone Number in use. Use another.'})
                        elif UserProfile.objects.filter(username = username):
                                return render(request, 'register.html', {'duplicate_message': 'Username Exists. Use another.'})                        
                
                        # No duplicate found, create and save the new record
                        user = UserProfile.objects.create(
                                first_name=first_name, 
                                last_name=last_name, 
                                email=email, 
                                phone_number=phone_number,
                                address=address, 
                                state=state, 
                                username=username, 
                                password=make_password(password),
                                profile_picture=profile_picture 
                        )
                
                        # Log in the user after successful registration
                        user = authenticate(username=username, password=password)
                        login(request, user)

                        return redirect('user_dashboard:dashboard_user')
        else:
                form = UserProfileForm()
        return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard:dashboard_admin')  # Redirect superusers to admin dashboard
        else:
            return redirect('user_dashboard:dashboard_user') 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
                login(request, user)
                if user.is_superuser:
                        return redirect('admin_dashboard:dashboard_admin')  # Redirect superusers to admin dashboard
                else:
                        return redirect('user_dashboard:dashboard_user')
        else:
                # Authentication failed, display error message
                return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'login.html', {})