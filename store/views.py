from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


# Create your views here.
def product(request, pk):
    # fetch the product with the given primary key (pk) from the database
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    # render the product.html template with the product data
    return render(request, 'product.html', {'product': product, 'categories': categories})

def category(request, cn):
    cn = cn.replace('-', ' ')  # Replace hyphens with spaces to match category names
    try:
        category = Category.objects.get(name__iexact=cn)  # Case-insensitive match
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        return render(request, 'category.html', {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        messages.success(request, "Category not found.")
        return redirect('home')
    
    
def home(request):
    # fetch all products from database
    products = Product.objects.all()
    categories = Category.objects.all()
    # render the home.html template with products data
    return render(request, 'home.html', {'products': products, 'categories': categories})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: # User is authenticated
            login(request, user)
            messages.success(request, ("You have successfully logged in."))
            return redirect('home') # Redirect to home page after login
        else:
            messages.success(request, ("Error logging in. Please try again..."))
            return redirect('login')
    else:
        categories = Category.objects.all()
        return render(request, 'login.html', {'categories': categories}) # Render the login form    

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... Thanks"))
    return redirect('home') # Redirect to home page after logout

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and log in the user after successful registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') # password1 is the first password field in UserCreationForm
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful. You are now logged in."))
            return redirect('home') # Redirect to home page after registration
        else:
            messages.success(request, ("Unsuccessful registration. Invalid information."))
            return redirect('register')
    categories = Category.objects.all()
    return render(request, 'register.html', {'form': form, 'categories': categories}) # Render the registration form

# Note: The login_user and logout_user views are placeholders and need to be implemented with actual authentication logic.