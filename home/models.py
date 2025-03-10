from django.db import models
from django.conf import settings
# Create your models here.

from django.db import models

class Appointment(models.Model):
    full_name = models.CharField(max_length=255)
    pickup_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    book_condition = models.CharField(max_length=50)
    quantity = models.IntegerField()
    address = models.TextField()
    book_category = models.CharField(max_length=100)
    expected_amount = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.pickup_date}"


class ContactAdmin(models.Model):
    name = models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    message=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def discount_percentage(self):
        if self.mrp > 0:
            return round(((self.mrp - self.discounted_price) / self.mrp) * 100, 2)
        return 0

    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    is_in_stock = models.BooleanField(default=True)  # New field for stock status

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
