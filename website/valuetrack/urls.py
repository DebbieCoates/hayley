
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
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
    # path('problem_add/<int:customer_id>/', views.problem_add, name='problem_add')
    
    path('problem_add/', views.problem_add, name='problem_add'),
    path('problem_add/<int:customer_id>/', views.problem_add_from_customer, name='problem_add_from_customer'),
]
