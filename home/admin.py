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
