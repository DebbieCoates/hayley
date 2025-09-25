from django.contrib import admin
from .models import Customer, ProblemStatement, Provider,Service, ServiceProvider

# Register your models here.
admin.site.register(Customer)
admin.site.register(ProblemStatement)
admin.site.register(Provider)
admin.site.register(Service)
admin.site.register(ServiceProvider)