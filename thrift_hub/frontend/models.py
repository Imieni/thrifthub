from django.db import models
from user_dashboard.models import Sales
from accounts.models import UserProfile
import secrets
from .paystack import Paystack

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Sales, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s CartItem: {self.product.name}"
    

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Sales)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Order.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
    
class Verified_Sales(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seller_id = models.BigIntegerField()
    product = models.ForeignKey(Sales, on_delete=models.CASCADE)
    date_of_sale = models.DateTimeField(auto_now_add=True)
