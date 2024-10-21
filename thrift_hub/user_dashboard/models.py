from django.db import models
from admin_dashboard.models import Category
from accounts.models import UserProfile
from django.utils.text import slugify

# Create your models here.
class Sales(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, unique=True, editable=False) 
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20)
    description = models.TextField(default='No description')
    image = models.ImageField(upload_to='sales_images/')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=2)

    def save(self, *args, **kwargs):
        # Generate SKU if not already set
        if not self.sku:
            count = Sales.objects.count()
            self.sku = f"THB{str(count + 1).zfill(5)}"
            combined_text = f"{self.product_name} {self.sku}"
            self.slug = slugify(combined_text)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.product_name
    

class GalleryMedia(models.Model):
    product = models.ForeignKey(Sales, related_name='gallery_media', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sales_images/')  

    def __str__(self):
        return f"Media for {self.product.product_name}"