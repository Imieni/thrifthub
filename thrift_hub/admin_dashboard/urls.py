from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('dashboard-admin', views.dashboard_admin, name='dashboard_admin'),
    path('add-category', views.add_category, name='add_category'),
    path('all-category', views.all_category, name='all_category'),
    path('logout/', views.logout_view, name='logout'),
    path('category/category-detail/<slug:slug>', views.category_detail, name='category_detail'),
    path('users/all-users', views.all_users, name='all_users'),
    path('users/add-user', views.add_user, name='add_user'),
    path('users/user-detail/<str:username>', views.user_detail, name='user_detail'),
    path('account/revenue', views.revenue, name='revenue'),
    path('revenue/product-detail/<slug:slug>', views.product_detail, name='product_detail'),

]