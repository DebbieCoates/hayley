from django.contrib import admin
from .models import Customer, ProblemStatement

# Register your models here.
admin.site.register(Customer)
admin.site.register(ProblemStatement)
