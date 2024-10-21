from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from user_dashboard.models import Sales
from admin_dashboard.models import Category
from frontend.models import Cart, Order, Verified_Sales
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.conf import settings

# Create your views here.
def index(request):
    products = Sales.objects.filter(status='available').order_by('-id')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'frontend/index.html', context)

def product_detail(request, slug):
    return render(request, 'frontend/index.html')

def category_listing(request):
    return render(request, 'frontend/index.html')

# def add_to_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product_price = request.POST.get('product_price')
#         # Perform validation and add the product to the cart
#         if 'cart' not in request.session:
#             request.session['cart'] = []
#         #product_info = {'product_id': product_id, 'product_price': product_price}
#         request.session['cart'].append(product_id)
#         #request.session['cart'].append(product_price)
#         request.session.modified = True  # Ensure session is saved
#     return redirect('frontend:cart') 

# def cart_items(request):
#     cart = request.session.get('cart', [])  # Retrieve the cart from the session
#     #cart_ids = [int(item) for item in cart]
#     products = Sales.objects.filter(id__in=cart)  # Query products based on cart items
    

#     context = {
#         'products': products
#     }
#     return render(request, 'frontend/cart.html', context)

def add_to_cart(request,pk):
    product = Sales.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(product=product, user=request.user)

    if not created:
        return redirect('frontend:cart')
    return redirect('frontend:cart') 

def cart_items(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    subtotal = 0
    for item in cart_items:
        subtotal += item.product.product_price
    total = subtotal + 2000
    

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }
    return render(request, 'frontend/cart.html', context)

@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        cart_items = Cart.objects.filter(user=user)
        products = []
        total_amount = 2000
        for cart_item in cart_items:
            total_amount += cart_item.product.product_price
            products.append(cart_item.product)
        
        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Order.objects.create(amount=total_amount, email=email, user=request.user)
        payment.products.set(products)
        payment.save()
        

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'products': products
        }
        return render(request, 'frontend/make_payment.html', context)

        #print("Cart Products:", cart_products)

    return render(request, 'frontend/cart.html')

def verify_payment(request, ref):
    payment = Order.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        cart_items = Cart.objects.filter(user=request.user)

        # Move cart items to Verified_Sales and delete cart items
        for cart_item in cart_items:
            Verified_Sales.objects.create(
                buyer=cart_item.user,
                seller_id=cart_item.product.user_id,
                product=cart_item.product,
            )
        cart_items.delete()
        for product in payment.products.all():
            #product.delete()
            product.status = 'sold'
            product.save()
        return redirect('frontend:cart')
    return redirect('frontend:cart')
    
def calculate_total_amount(cart_products):
    total_amount = Decimal(0)
    for product in cart_products:
        price = Decimal(product)
        total_amount += product.price
    return total_amount

def delete_item(request,pk):
    item = get_object_or_404(Cart, pk=pk)
    item.delete()
    return redirect('frontend:cart')