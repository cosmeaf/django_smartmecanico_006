from django.db import models
from dashboard.models.base_model import Base
from dashboard.models.user_model import CustomUser
from dashboard.models.address_model import Address


class Product(Base):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(Base):
    user = models.ForeignKey(CustomUser, verbose_name='Usuário', on_delete=models.CASCADE, related_name='Customer')
    address = models.ForeignKey(Address, verbose_name='Endereço', on_delete=models.CASCADE, related_name='Customer', related_query_name="Customer")

    def __str__(self):
        return self.user.get_full_name() or self.user.email

class Order(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(Base):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

class Payment(Base):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=100)  # Ex: 'Credit Card', 'PayPal', 'Bank Transfer', etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id}"
