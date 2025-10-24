from django.urls import path
from . import views

urlpatterns = [
    
    path('summary', views.cart_summary, name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'), 
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('place_order/', views.place_order, name='place_order'),
    path('success/', views.order_success, name='order_success'),
    path('cart/paystack/checkout/', views.paystack_checkout, name='paystack_checkout'),
    path('payment_verify/', views.payment_verify, name='payment_verify'),
    path('checkout/', views.checkout, name='checkout'),

    

]




    

