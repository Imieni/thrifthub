from django.shortcuts import render, redirect
from .models import Category
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard_admin(request):
    return render(request, 'admin-templates/dashboard.html')

@login_required
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