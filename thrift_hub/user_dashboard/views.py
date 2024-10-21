from django.shortcuts import render, get_object_or_404, redirect
from .models import Sales, GalleryMedia
from accounts.models import UserProfile
from admin_dashboard.models import Category
from frontend.models import Verified_Sales
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404


# Create your views here.
@login_required
def dashboard_user(request):
    return render(request, 'user-templates/user-profile.html')

def handle_uploaded_file(file):
    # Save the uploaded file to the appropriate location
    with open('media/sales_images' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

@login_required
def add_product(request):
    if request.method == 'POST' and request.FILES:
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price').replace(',', '')
        category_id = request.POST.get('category')
        status= request.POST.get('status')
        product_image = request.FILES.get('product_image')
        description = request.POST.get('description')
        user_id = request.user.id

        category_instance = Category.objects.get(pk=category_id)

        new_product = Sales(product_name=product_name, product_price=product_price, status=status, image=product_image, description=description, user_id=user_id)
        #new_product.save(commit=False)
        new_product.category = category_instance


        # Handle gallery media
        for file in request.FILES.getlist('file'):
            # Save each uploaded file to the appropriate location
            handle_uploaded_file(file)

            # Associate the file with the product
            GalleryMedia.save(image='sales_images/' + file.name)
        
        new_product.save()
        #new_product.save()

        return render(request, 'user-templates/add-product.html', {'success_message' : 'New Product added successfully!'})
    categories = Category.objects.all()
    return render(request, 'user-templates/add-product.html', {'categories':categories})

@login_required
def upload_sales_images(request):
    # Handle file uploads and save them to the server
    # Example implementation:
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        # Process the uploaded file...
        return JsonResponse({'message': 'File uploaded successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method or no files uploaded'}, status=400)

@login_required
def all_products(request):
    products = Sales.objects.filter(user_id=request.user.id)
    return render(request, 'user-templates/products.html', {'products':products})

@login_required
def product_detail(request, slug):
    # Retrieve the Sales object with the given slug from the database
    product = get_object_or_404(Sales, slug=slug)
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories
    }

    # Render the template with the Sales object
    return render(request, 'user-templates/edit-product.html', context)

@login_required
def update_product(request, slug):
    # Retrieve the existing product instance
    product = get_object_or_404(Sales, slug=slug)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.product_price = request.POST.get('product_price').replace(',', '')
        category_id = request.POST.get('category')
        product.status= request.POST.get('status')
        #product.image = request.FILES.get('product_image')
        product.description = request.POST.get('description')
        
        category_instance = Category.objects.get(pk=category_id)
        product.category = category_instance
        
        if request.FILES.get('product_image'):
            product.image = request.FILES['product_image']
        else:
            product.image = product.image

        product.save()
        messages.success(request, 'Product "' + product.product_name + '" successfully updated!')
        return redirect('user_dashboard:all_products')
    
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
        'slug': slug
    }
    return render(request, 'user-templates/edit-product.html', context)

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def user_profile(request):
    return render(request, 'user-templates/user-profile.html')

@login_required
def user_setting(request):
    # Retrieve the existing user instance
    user = get_object_or_404(UserProfile, id=request.user.id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number= request.POST.get('phone_number')
        user.state = request.POST.get('state')
                
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        else:
            user.profile_picture = user.profile_picture

        user.save()
        messages.success(request, 'Thrifter @' + user.username + ' successfully updated!')
        return redirect('user_dashboard:user_setting')
        
    context = {
        'user': user,
    }
    return render(request, 'user-templates/user-setting.html', context)

@login_required
def all_orders(request):
    verified_sales = Verified_Sales.objects.filter(seller_id=request.user.id)

    for sale in verified_sales:
        sale.product_details = sale.product
        sale.user_details = sale.buyer

    context = {
        'verified_sales': verified_sales
    }
    return render(request, 'user-templates/orders.html', context)

@login_required
def all_purchases(request):
    verified_sales = Verified_Sales.objects.filter(buyer_id=request.user.id)

    for sale in verified_sales:
        sale.product_details = sale.product
        sale.user_details = UserProfile.objects.get(id=sale.seller_id)

    context = {
        'verified_sales': verified_sales
    }

    return render(request, 'user-templates/purchases.html', context)

@login_required
def buyer(request, username):
    try:
        buyer = UserProfile.objects.get(username=username)

    except UserProfile.DoesNotExist:
        # If user does not exist, raise a 404 error
        raise Http404("User " + username + " does not exist")

    return render(request, 'user-templates/buyer.html', {'buyer': buyer})

@login_required
def seller(request, username):
    try:
        seller = UserProfile.objects.get(username=username)

    except UserProfile.DoesNotExist:
        # If user does not exist, raise a 404 error
        raise Http404("User " + username + " does not exist")

    return render(request, 'user-templates/seller.html', {'seller': seller})