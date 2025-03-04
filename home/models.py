from django.db import models

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
    

