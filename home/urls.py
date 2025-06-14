from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home,name='home'),
    path('sellbooks',views.sellbooks,name='sellbooks'),
    path('contact/',views.contact,name='contact'),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("contact_admin/",views.contact_admin,name="contact_admin"),
    path("buybooks",views.buybooks,name='buybooks'),
    path("novels/",views.novels,name='novels'),
    path("personaldevelopment/",views.personaldevelopment,name='personaldevelopment'),
    path("academic/",views.academic,name='academic'),
    path("cart/",views.cart_view,name='cart'),
    path("profile",views.profile_view,name='profile'),
    path('order-item/<int:id>/', views.add_to_cart, name='OrderItem'),
    path("buy",views.buy, name='buy'),
    path('checkout/', views.checkout, name='checkout'),
    path('rzp-button',views.payment_view, name='rzp-button'),

    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('verify-otp/', views.otp_verify_view, name='otp_verify'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='home/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password/password_reset_complete.html'),
         name='password_reset_complete'),




    


    
    
]