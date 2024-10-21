from django.shortcuts import render, redirect
from django.http import JsonResponse
from user_dashboard.models import Sales
from admin_dashboard.models import Category
from frontend.models import Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

# Create your views here.
def index(request):
    products = Sales.objects.all().order_by('-id')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'frontend/index.html', context)

def product_detail(request):
    return render(request, 'frontend/index.html')

def category_listing(request):
    return render(request, 'frontend/index.html')

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_price = request.POST.get('product_price')
        # Perform validation and add the product to the cart
        if 'cart' not in request.session:
            request.session['cart'] = []
        #product_info = {'product_id': product_id, 'product_price': product_price}
        request.session['cart'].append(product_id)
        #request.session['cart'].append(product_price)
        request.session.modified = True  # Ensure session is saved
    return redirect('frontend:cart') 

def cart_items(request):
    cart = request.session.get('cart', [])  # Retrieve the cart from the session
    #cart_ids = [int(item) for item in cart]
    products = Sales.objects.filter(id__in=cart)  # Query products based on cart items
    

    context = {
        'products': products
    }
    return render(request, 'frontend/cart.html', context)

@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart_products = request.session.get('cart', [])

        #print("Cart Products:", cart_products)

        

    return render(request, 'frontend/test.html', {'cart_products': cart_products})
    
def calculate_total_amount(cart_products):
    total_amount = Decimal(0)
    for product in cart_products:
        price = Decimal(product)
        total_amount += product.price
    return total_amount