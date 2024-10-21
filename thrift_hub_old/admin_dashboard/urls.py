from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-admin', views.dashboard_admin, name='dashboard_admin'),
    path('add-category', views.add_category, name='add_category')
]