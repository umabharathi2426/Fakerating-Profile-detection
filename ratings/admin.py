# Register your models here.
from django.contrib import admin
from .models import Product, Rating
from accounts.models import *

admin.site.register(Product)
