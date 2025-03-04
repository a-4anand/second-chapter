from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('sellbooks',views.sellbooks),
    path('contact/',views.contact),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("contact_admin/",views.contact_admin,name="contact_admin")
]