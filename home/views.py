from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import AppointmentForm, ContactAdminForm
from .models import Appointment, ContactAdmin, Book, OrderItem, Address
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
def home(request):
    return render(request, 'home/home.html')


def send_otp_email(email, otp):
    subject = "Your OTP for Registration"
    message = f"Your OTP for registration is {otp}. Please do not share this with anyone."
    from_email = "your-email@example.com"  # Update with your email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def user_register(request):
    if request.method == 'POST':
        # Get data from the registration form
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email:
            return render(request, 'home/main/register.html', {
                "error": "Email is required"
            })

        # Generate OTP and send it via email
        otp = random.randint(100000, 999999)
        send_otp_email(email, otp)

        # Store the OTP and email in the session
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['username'] = username
        request.session['password1'] = password1
        request.session['password2'] = password2

        # Redirect to OTP verification page
        return redirect('otp_verify')

    # Initial form load for GET request
    form = UserCreationForm()
    return render(request, 'home/main/register.html', {
        "form": form
    })


def otp_verify_view(request):
    if request.method == 'POST':
        # Get OTP entered by the user
        otp_entered = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if not otp_entered:
            return render(request, 'home/password/otp-verify.html', {
                "error": "OTP is required"
            })

        # Validate OTP
        if otp_entered != str(stored_otp):
            return render(request, 'home/pasword/otp-verify.html', {
                "error": "Invalid OTP. Please try again."
            })

        # OTP is correct, so create the user
        email = request.session.get('email')
        username = request.session.get('username')
        password1 = request.session.get('password1')
        password2 = request.session.get('password2')

        # Create the user
        form = UserCreationForm({
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        })

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Clear OTP and session data
            request.session.pop('otp', None)
            request.session.pop('email', None)
            request.session.pop('username', None)
            request.session.pop('password1', None)
            request.session.pop('password2', None)

            return redirect('home')  # Redirect to home page or dashboard

        return render(request, 'home/password/otp-verify.html', {
            "error": "There was an issue with your registration."
        })

    # Show OTP form
    return render(request, 'home/password/otp-verify.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "home/main/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

def profile_view(request):
    return render(request,"home/main/profile.html", {'user': request.user})


def sellbooks(request):
    return render(request, 'home/main/addbook.html')


def contact(request):
    return render(request, 'home/main/contact.html')

@login_required(login_url='/login/')
def buybooks(request):
    books = Book.objects.all()
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False).values_list('item_id', flat=True)
    context = {
        'books': books,
        'cart_items': cart_items
    }

    return render(request, "home/main/buybook.html", context)


@login_required(login_url='/login/')
def academic(request):
    books = Book.objects.filter(category='Academic')
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False).values_list('item_id', flat=True)

    context = {
        'books': books,
        'cart_items': cart_items
    }

    return render(request, "home/main/buybook.html", context)

@login_required(login_url='/login/')

def personaldevelopment(request):
    books = Book.objects.filter(category='Personal Development')
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False).values_list('item_id', flat=True)

    context = {
        'books': books,
        'cart_items': cart_items
    }

    return render(request, "home/main/buybook.html", context)


@login_required(login_url='/login/')

def novels(request):
    books = Book.objects.filter(category='Novels')
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False).values_list('item_id', flat=True)

    context = {
        'books': books,
        'cart_items': cart_items
    }

    return render(request, "home/main/buybook.html", context)

@login_required(login_url='/login/')
def add_to_cart(request, id):
    book = get_object_or_404(Book, id=id)

    # Check if the item is already in the cart
    existing_order_item = OrderItem.objects.filter(user=request.user, item=book, ordered=False).first()

    if existing_order_item:
        messages.warning(request, "This item is already in your cart.")
    else:
        # Add item to cart
        order_item = OrderItem.objects.create(
            user=request.user,
            item=book,
            ordered=False
        )
        # Mark book as out of stock
        book.is_in_stock = False
        book.save()
        messages.success(request, f"{book.title} added to cart!")

    return redirect("cart") 

@login_required(login_url='/login/')
def cart_view(request):
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.item.discounted_price for item in cart_items) + 50

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, "home/main/cart.html", context)


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, user=request.user, ordered=False)
    item = order_item.item 
    order_item.delete()
    item.is_in_stock = True
    item.save()

    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.item.discounted_price for item in cart_items) + 50

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return redirect("cart")


def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Form submitted successfully!")
    else:
        form = AppointmentForm()
    return render(request, "home/main/addbook.html", {"form": form})

def checkout(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        landmark = request.POST.get('landmark', '')
        address_type = request.POST['address_type']

        # Create and save the address
        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            landmark=landmark,
            address_type=address_type
        )
        messages.success(request, "Address added successfully!")
        return redirect('checkout')

    return render(request, 'home/main/checkout.html')

def contact_admin(request):
    if request.method == "POST":
        form = ContactAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Message Sent")
    else:
        form = ContactAdminForm()

    return render(request, 'home/main/contact.html', {"form": form})



def buy(request):
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.item.discounted_price for item in cart_items) + 50

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request,"home/main/buy.html",context=context)