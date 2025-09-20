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
from .razorpay_integration import create_razorpay_order
import re
import razorpay
from django.conf import settings
from django.contrib import messages
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

        if not username:
            return render(request, 'home/main/register.html', {
                "error": "Username is required"
            })

        if len(password1) < 8:
            return render(request, 'home/main/register.html', {
                "error": "Password is too short."
            })
        if password1.isdigit():
            return render(request, 'home/main/register.html', {
                "error": "Password cannot be entirely numeric."
            })

        if password1.lower() in ['password', '12345678', 'qwerty', 'admin']:
            return render(request, 'home/main/register.html', {
                "error": "Password is too common."
            })

        if not re.search(r"[A-Za-z]", password1):
            return render(request, 'home/main/register.html', {
                "error": "Password must contain at least one letter."
            })

        if not re.search(r"[0-9]", password1):
            return render(request, 'home/main/register.html', {
                "error": "Password must contain at least one digit."
            })

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            return render(request, 'home/main/register.html', {
                "error": "Password must contain at least one special character."
            })

        if password1 != password2:
            return render(request, 'home/main/register.html',{
                "error": "Passwords does not match"
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
            return render(request, 'home/password/otp-verify.html', {
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

            request.session.pop('otp', None)
            request.session.pop('email', None)
            request.session.pop('username', None)
            request.session.pop('password1', None)
            request.session.pop('password2', None)

            return redirect('home')

        return render(request, 'home/password/otp-verify.html', {
            "error": "The Email is already registered or There was an issue with your registration."
        })


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
    addresses = Address.objects.filter(user=request.user)
    return render(request,"home/main/profile.html", {'user': request.user,'addresses': addresses})


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
            return redirect("success")
    else:
        form = AppointmentForm()
    return render(request, "home/main/addbook.html", {"form": form})

  # make sure Address is correctly imported

def success(request):
    return render(request, "home/main/success.html")


from .models import OrderItem, Address # Make sure Address is imported

def checkout(request):
    user = request.user

    # --- THIS WAS THE MISSING LINE ---
    # Check if an address for the current user already exists in the database.
    user_has_address = Address.objects.filter(user=user).exists()

    # Get cart and total
    cart_items = OrderItem.objects.filter(user=user, ordered=False)
    total_price = sum(item.item.discounted_price for item in cart_items) + 50

    # Razorpay setup
    # Note: For better security, store these keys in your project's settings.py file
    razorpay_key_id = "rzp_test_bS11AUD74lB4bg"
    razorpay_key_secret = "k9yV68xKelFwHMUYrSrSNZz"

    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
    amount = int(total_price * 100)  # Amount in paise (e.g., ₹500.50 -> 50050)
    currency = 'INR'

    payment_order = client.order.create({
        'amount': amount,
        'currency': currency,
        'payment_capture': 1
    })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': razorpay_key_id,
        'amount': amount,
        'order_id': payment_order['id'],
        'show_address_form': not user_has_address  # Now this variable will work correctly
    }

    return render(request, 'home/main/checkout.html', context)



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
    user = request.user

    user_has_address = Address.objects.filter(user=user).exists()

    if request.method == 'POST' and not user_has_address:
        # Save new address
        Address.objects.create(
            user=user,
            full_name=request.POST['full_name'],
            phone_number=request.POST['phone_number'],
            street_address=request.POST['street_address'],
            city=request.POST['city'],
            state=request.POST['state'],
            postal_code=request.POST['postal_code'],
            landmark=request.POST.get('landmark', ''),
            address_type=request.POST['address_type']
        )
        messages.success(request, "Address added successfully!")
        return redirect('checkout')

    elif request.method == 'POST':
        messages.info(request, "Address already exists.")
        return redirect('checkout')

    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.item.discounted_price for item in cart_items) + 50

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request,"home/main/buy.html",context=context)






def payment_view(request):
    # Replace with your actual Razorpay Key ID and Secret
    razorpay_key_id = "rzp_test_bS11AUD74lB4bg"
    razorpay_key_secret = "k9yV68xKelFwHMUYrSrSNZz"

    # Import Razorpay Python package

    client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

    amount = 50000  # in paise => ₹500
    currency = 'INR'
    payment_order = client.order.create(dict(amount=amount, currency=currency, payment_capture=1))
    order_id = payment_order['id']

    context = {
        'razorpay_key_id': razorpay_key_id,
        'amount': amount,
        'order_id': order_id
    }
    return render(request, 'home/main/checkout.html', context)
