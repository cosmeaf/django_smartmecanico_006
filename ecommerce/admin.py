from django.contrib import admin
from .models import Product, Customer, Order, OrderItem, Payment

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
