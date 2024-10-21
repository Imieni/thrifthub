from django.db import models
from user_dashboard.models import Sales
from accounts.models import UserProfile
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Sales, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s CartItem: {self.product.name}"
    

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Sales)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
