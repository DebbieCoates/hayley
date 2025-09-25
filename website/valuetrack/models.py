from django.db import models
from django.contrib.auth.models import User

ProviderStatus_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),]
    
ProviderType_CHOICES = [
        ('Internal', 'Internal'),
        ('External', 'External'),
        ('Partner', 'Partner')
    ]
Industry_CHOICES = [
        ('Tech', 'Technology'), 
        ('Finance', 'Finance'), 
        ('Health', 'Healthcare'), 
        ('Edu', 'Education'), 
        ('Retail', 'Retail'),
        ('Eng', 'Engineering'),
        ('Auto', 'Automotive'),
        ('Food', 'Food & Beverage'),
        ('Media', 'Media & Entertainment'),
        ('Con', 'Construction'),
        ('Other', 'Other')
    ]

location_CHOICES = [
        ('East of England', 'East of England'), 
        ('East Midlands', 'East Midlands'), 
        ('London', 'London'), 
        ('North East', 'North East'), 
        ('North West', 'North West'),
        ('South East', 'South East'),
        ('South West', 'South West'),  
        ('West Midlands', 'West Midlands'),
        ('Yorkshire and the Humber', 'Yorkshire and the Humber'),
        ('Scotland', 'Scotland'),
        ('Wales', 'Wales'),
        ('Northern Ireland', 'Northern Ireland'),
        ('Other', 'Other')
    ]

status_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending', 'Pending'),
        ('Archived', 'Archived'),
        ('Prospect', 'Prospect'),
        ('Other', 'Other')
    ]
Urgency_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical')
    ]  
ProblemStatus_CHOICES = [ 
            ('Open', 'Open'),
            ('In Progress', 'In Progress'),
            ('Resolved', 'Resolved'),
            ('Closed', 'Closed')
        ]  
       
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    main_contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=100, choices=Industry_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=100, choices=location_CHOICES, blank=True, null=True)
    account_manager = models.CharField(max_length=100, blank=True, null=True)   
    status = models.CharField(max_length=50, choices=status_CHOICES, blank=True, null=True, default='Active')
    notes = models.TextField(blank=True, null=True) 
    logo = models.ImageField(upload_to='customer_logos/', blank=True, null=True)
    # ✅ Audit Trail   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
   

    def __str__(self):
        return self.name
    
class ProblemStatement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='problem_statements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    impact = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=50, choices=Urgency_CHOICES, blank=True, null=True, default='Medium')
    status = models.CharField(max_length=50, choices=ProblemStatus_CHOICES, blank=True, null=True, default='Open')
    notes = models.TextField(blank=True, null=True) 
    # ✅ Audit Trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.title} - {self.customer.name}"
    
class Provider(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ProviderType_CHOICES, default='External')
    department = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=ProviderStatus_CHOICES, default='Active')
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, choices=Industry_CHOICES, blank=True, null=True, default='Other')
    # services_offered = models.TextField(blank=True, null=True)  

    # ✅ Tagging
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords (e.g. IT, Logistics, Europe)")

    # ✅ Audit Trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='providers_created')

    def __str__(self):
        return f"{self.name} ({self.type})"
