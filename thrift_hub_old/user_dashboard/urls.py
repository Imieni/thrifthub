from django.urls import path
from . import views 
from accounts.views import login_view

app_name = 'user_dashboard'

urlpatterns = [
    path('dashboard', views.dashboard_user, name='dashboard_user'),
    path('products/add-product', views.add_product, name='add_product'),
    path('media/sales_images', views.upload_sales_images, name='upload_sales_images'),
    path('products', views.all_products, name='all_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/update_product/<slug:slug>', views.update_product, name='update_product'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('user/user-profile/', views.user_profile, name='user_profile'),
    path('user/user-setting/', views.user_setting, name='user_setting'),
]