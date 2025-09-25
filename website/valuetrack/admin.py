from django.contrib import admin
from .models import Customer, ProblemStatement, Provider, Category, Service, Solution, ProblemSolutionLink
from django.contrib.auth.models import User
from django.db import models


# Register your models here.
admin.site.register(Customer)
admin.site.register(ProblemStatement)
admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Solution)
admin.site.register(ProblemSolutionLink)
