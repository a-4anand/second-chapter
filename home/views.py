from django.shortcuts import render
from django.http import HttpResponse
 
def home(request):
    return render(request, 'home/home.html')


def sellbooks(request):
    return render(request,'home/main/addbook.html')


def contact(request):
    return render(request,'home/main/contact.html')