from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import AppointmentForm,ContactAdminForm
from django.shortcuts import render, redirect
from .models import Appointment,ContactAdmin  # Import your model
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'home/home.html')


def sellbooks(request):
    return render(request,'home/main/addbook.html')


def contact(request):
    return render(request,'home/main/contact.html')


def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Form submitted")  # Change 'success_page' to your success URL
    else:
        form = AppointmentForm()

    return render(request, "home/main/addbook.html", {"form": form})

def contact_admin(request):
    if request.method == "POST":
        form = ContactAdminForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse ("Message Sent")
    else:
        form = ContactAdminForm()

    return render (request,'home/main/contact.html',{"from":form})    

# def book_appointment(request):
#     if request.method == "POST":
#         full_name = request.POST.get('full_name')
#         pickup_date = request.POST.get('pickup_date')
#         time_slot = request.POST.get('time_slot')
#         mobile_number = request.POST.get('mobile_number')
#         book_condition = request.POST.get('book_condition')
#         quantity = request.POST.get('quantity')
#         address = request.POST.get('address')
#         book_category = request.POST.get('book_category')
#         expected_amount = request.POST.get('expected_amount', '')
#         city = request.POST.get('city')
#         additional_comments = request.POST.get('additional_comments', '')

#         # Handle file upload
#         photo = request.FILES.get('book_photo')
#         if photo:
#             fs = FileSystemStorage()
#             photo_path = fs.save(photo.name, photo)
#         else:
#             photo_path = None

#         # Save data in the database
#         Appointment.objects.create(
#             full_name=full_name,
#             pickup_date=pickup_date,
#             time_slot=time_slot,
#             mobile_number=mobile_number,
#             book_condition=book_condition,
#             quantity=quantity,
#             address=address,
#             book_category=book_category,
#             expected_amount=expected_amount,
#             city=city,
#             book_photo=photo_path,
#             additional_comments=additional_comments
#         )

#         return HttpResponse("SUbmitted")  # Redirect after successful submission

#     return render(request, "home/main/addbook.html")
