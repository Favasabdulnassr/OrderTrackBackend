from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Order Placed', 'Order Placed'),
        ('Ready to Dispatch', 'Ready to Dispatch'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    user_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Order Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
