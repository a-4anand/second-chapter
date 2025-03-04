from django.contrib import admin
from .models import Appointment,ContactAdmin # Import your model

admin.site.register(Appointment)  # Register the model
admin.site.register(ContactAdmin)