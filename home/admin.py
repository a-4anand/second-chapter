from django.contrib import admin
from .models import Appointment,ContactAdmin,Book

admin.site.register(Appointment)  # Register the model
admin.site.register(ContactAdmin)
admin.site.register(Book)


from django.contrib import admin
from .models import Book

# Unregister if already registered
try:
    admin.site.unregister(Book)
except admin.sites.NotRegistered:
    pass

# Register the model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_in_stock')  # Customize as needed

# home/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Book, Address


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the order list
    list_display = (
        'razorpay_order_id',
        'user',
        'total_amount',
        'status',  # ✅ Show the status
        'is_paid',
        'ordered_date'
    )

    # ✅ This makes the 'status' field an editable dropdown in the list
    list_editable = ['status']

    # Add filters for easier navigation
    list_filter = ('status', 'is_paid', 'ordered_date')

    # Add search functionality
    search_fields = ('user__username', 'razorpay_order_id')