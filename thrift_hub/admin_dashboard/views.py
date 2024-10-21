from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from user_dashboard.models import UserProfile
from frontend.models import Verified_Sales
from .utils import admin_required
from django.contrib.auth import logout
from accounts.forms import UserProfileForm
from django.contrib.auth.hashers import make_password
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@admin_required
def dashboard_admin(request):
    return render(request, 'admin-templates/admin-profile.html')

@admin_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        existing_record = Category.objects.filter(category_name=category_name).exists()

        if existing_record:
            # Duplicate registration found, handle accordingly
            return render(request, 'admin-templates/add-category.html', {'duplicate_message': 'Category Exists in database.'})
        new_category = Category(category_name=category_name)
        new_category.save()
        return render(request, 'admin-templates/add-category.html', {'success_message' : 'Category added successfully!'})
    return render(request, 'admin-templates/add-category.html')

@admin_required
def all_category(request):
    categories = Category.objects.all()
    return render(request, 'admin-templates/category.html', {'categories':categories})


@admin_required
def category_detail(request, slug):
    # Retrieve the Sales object with the given slug from the database
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()

    context = {
        'category': category,
        'categories': categories
    }

    # Render the template with the Sales object
    return render(request, 'admin-templates/edit-category.html', context)

@admin_required
def add_user(request):
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
                    return render(request, 'admin-templates/add-user.html', {'duplicate_message': 'Email Exists. Use another.'})
            elif UserProfile.objects.filter(phone_number = phone_number):
                    return render(request, 'admin-templates/add-user.html', {'duplicate_message': 'Phone Number in use. Use another.'})
            elif UserProfile.objects.filter(username = username):
                    return render(request, 'admin-templates/add-user.html', {'duplicate_message': 'Username Exists. Use another.'})                        
    
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
        else:
            form = UserProfileForm()
        return render(request, 'admin-templates/add-user.html', {'form': form, 'success_message' : 'New User added successfully!' })

    return render(request, 'admin-templates/add-user.html')

@admin_required
def all_users(request):
    users = UserProfile.objects.filter(is_superuser=False).order_by('-id')

    context = {
        'users': users
    }

    return render(request, 'admin-templates/users.html', context)

@admin_required
def user_detail(request):
    users = UserProfile.objects.filter(user__is_superuser=False)

    context = {
        'users': users
    }

    return render(request, 'admin-templates/users.html', context)

@admin_required
def revenue(request):
    verified_sales = Verified_Sales.objects.all()

    for sale in verified_sales:
        sale.product_details = sale.product
        seller_commission = sale.product.product_price

    context = {
        'verified_sales': verified_sales,
        'seller_commission':seller_commission
    }

    return render(request, 'admin-templates/revenue.html', context)


@admin_required
def product_detail(request):
    users = UserProfile.objects.filter(user__is_superuser=False)

    context = {
        'users': users
    }

    return render(request, 'admin-templates/users.html', context)
