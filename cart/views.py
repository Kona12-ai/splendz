from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .cart import Cart
from .models import Order, OrderItem
from store.models import Product
from django.contrib import messages 
from django.conf import settings
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction


# Cart Summary Page

def cart_summary(request):
    cart = Cart(request)
    products_in_cart = list(cart)  # Convert to list so iteration works
    cart_total = cart.get_total_price()

    return render(request, 'cart/cart_summary.html', {
        'products_in_cart': products_in_cart,
        'cart_total': cart_total,
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_summary')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_summary')

def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect('cart_summary')


def cart_increase(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, qty=1, update_qty=False)
    return JsonResponse({
        "success": True,
        "qty": len(cart)
    })




def checkout(request):
    cart = Cart(request)
    cart_items = []
    total_price = 0

    for item in cart:
        subtotal = item['total_price']
        total_price += subtotal
        cart_items.append({
            'product': item['product'],
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })




def place_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()  # now this will work
        messages.success(request, "Order placed successfully!")
        return redirect('store')  # or redirect to a 'success' page
    return redirect('cart_summary')



        
def order_success(request):
    return render(request, 'cart/order_success.html')



paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

def paystack_checkout(request):
    cart = Cart(request)
    total_price = cart.get_total_price()  # your cart total
    
    # Convert to kobo (Paystack uses the smallest currency unit)
    amount_kobo = int(total_price * 100)
    
    user_email = request.user.email if request.user.is_authenticated else 'guest@example.com'
    
    # Initialize transaction
    response = Transaction.initialize(
        email=user_email,
        amount=amount_kobo,
        callback_url=request.build_absolute_uri('/cart/payment_verify/')
    )
    
    if response['status']:
        return redirect(response['data']['authorization_url'])
    else:
        # Handle initialization error
        return render(request, 'cart/payment_error.html', {'message': response['message']})
    

def payment_verify(request):
    reference = request.GET.get('reference', '')
    if not reference:
        return render(request, 'cart/payment_error.html', {'message': 'No reference provided.'})
    
    response = Transaction.verify(reference)
    
    if response['status'] and response['data']['status'] == 'success':
        # Payment successful, clear cart, save order, etc.
        cart = Cart(request)
        cart.clear()  # clear the cart after successful payment
        return render(request, 'cart/payment_success.html', {'cart_items': cart.get_prods()})
    else:
        return render(request, 'cart/payment_error.html', {'message': 'Payment failed.'})



# def cart_summary(request):
#     cart = Cart(request)
#     cart_products = []
#     total_price = 0

#     for product in cart.get_prods():
#         quantity = cart.cart[str(product.id)]['quantity']
#         price = float(cart.cart[str(product.id)]['price'])
#         subtotal = price * quantity
#         total_price += subtotal

#         cart_products.append({
#             'product': product,
#             'quantity': quantity,
#             'subtotal': subtotal,
#         })

#     context = {
#         'cart_products': cart_products,
#         'total_price': total_price,
#     }
#     return render(request, 'cart_summary.html', context)

# def cart_summary(request):
#     cart = Cart(request)
#     cart_products = cart.get_prods()
#     return render(request, 'cart_summary.html', {'cart_products': cart_products})

# def cart_add(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         product_id = request.POST.get('productid')
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product=product)
#         cart_quantity = len(cart)
#         return JsonResponse({'qty': cart_quantity})
#     return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    return JsonResponse({'message': 'Delete functionality coming soon!'})


def cart_update(request):
    return JsonResponse({'message': 'Update functionality coming soon!'})


# def cart_add(request):
#     cart = Cart(request)

#     if request.method == 'POST':
#         product_id = request.POST.get('productid')
#         product_qty = request.POST.get('productqty')

#         if not product_id:
#             return JsonResponse({'error': 'No product ID provided'}, status=400)

#         product = get_object_or_404(Product, id=product_id)

#         cart.add(product=product)
#         cart_quantity = len(cart)
#         return JsonResponse({'qty': cart_quantity})

#     return JsonResponse({'error': 'Invalid request'}, status=400)



# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from .cart import Cart
# from store.models import Product


# # Create your views here.
# def cart_summary(request):
#     cart = Cart(request)
#     cart_products = cart.get_prods
#     return render(request, 'cart_summary.html', {'cart_products': cart_products})

# def cart_add(request):

#     cart = Cart(request)
#     if request.method == 'POST':
#         product_id = request.POST.get('productid')
#         product_qty = request.POST.get('productqty')
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product=product)
#         cart_quantity = cart.__len__()
#         response = JsonResponse({'qty': cart_quantity})
#         return response
#     # return render(request, 'cart_add.html', {})
    

# def cart_delete(request):

#     pass
#     # return render(request, 'cart_delete.html', {})

# def cart_update(request):
#     pass
#     # return render(request, 'cart_update.html', {})