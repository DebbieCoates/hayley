
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name='home'),# Home page
    path('', views.customer_list, name='home'),
    
    path('about/', views.about, name='about'),
    
    # Customer URLs
    path('customers/', views.customer_list, name='customers'),
    path('customer/<int:customer_id>/', views.customer, name='customer'),
    path('customer_delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('customer_edit/<int:customer_id>/', views.customer_edit, name='customer_edit'),
    path('customer_add/', views.customer_add, name='customer_add'),  # New URL pattern for adding a customer
    
    # Authentication URLs
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    
    # Problem Statement URLs
    path('problems/', views.problem_list, name='problems'),
    path('problem/<int:problem_id>/', views.problem, name='problem'),
    path('problem_delete/<int:problem_id>/', views.problem_delete, name='problem_delete'),
    path('problem_edit/<int:problem_id>/', views.problem_edit, name='problem_edit'),
    path('problem_add/', views.problem_add, name='problem_add'),
    path('problem_add/<int:customer_id>/', views.problem_add_from_customer, name='problem_add_from_customer'),
    
    # Provider URLs
    path('providers/', views.provider_list, name='providers'),
    path('provider/<int:provider_id>/', views.provider, name='provider'),
    path('provider_delete/<int:provider_id>/', views.provider_delete, name='provider_delete'),
    path('provider_edit/<int:provider_id>/', views.provider_edit, name='provider_edit'),
    path('provider_add/', views.provider_add, name='provider_add'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category_add/', views.category_add, name='category_add'),
    path('category_edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category_delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Service URLs
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
]

  
