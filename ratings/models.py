from django.db import models
from accounts.models import User
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')  # Save images in this folder

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time_taken = models.CharField(max_length=20, null=True, blank=True)  # Store time in format "Xm Ys"

    def __str__(self):
        return f"{self.user} - {self.product} - {self.rating}"
