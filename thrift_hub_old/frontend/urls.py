from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
        path('', views.index, name='index'),
        path('product/<slug:slug>/', views.product_detail, name='product_detail'),
        path('category/<slug:slug>/', views.category_listing, name='category_listing'),
        path('add_to_cart', views.add_to_cart, name='add_to_cart'),
        path('cart/', views.cart_items, name='cart'),
        path('place_order/', views.place_order, name='place_order'),

]