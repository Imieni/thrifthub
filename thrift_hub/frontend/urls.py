from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
        path('', views.index, name='index'),
        path('product/<slug:slug>/', views.product_detail, name='product_detail'),
        path('category/<slug:slug>/', views.category_listing, name='category_listing'),
        path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
        path('cart/', views.cart_items, name='cart'),
        path('delete_item/<int:pk>', views.delete_item, name='delete_item'),
        path('place_order/', views.place_order, name='place_order'),
        path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),

]