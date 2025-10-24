from decimal import Decimal
from store.models import Product
from django.conf import settings

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add or update product in cart."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': float(product.price),
                'quantity': 0
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """Mark session as modified."""
        self.session.modified = True

    def remove(self, product):
        """Remove product from cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrease(self, product):
        """Decrease product quantity."""
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate through cart items and attach Product objects (without saving them in session)."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()  # ✅ work on a copy to avoid saving Product objects

        for product in products:
            item = cart[str(product.id)].copy()  # ✅ copy each item dict
            item['product'] = product
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Get total cost of all items in cart."""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Empty the cart."""
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True






  
    # def get_total_price(self):
    #     return sum(float(item['price']) * item['quantity'] for item in self.cart.values())


# from store.models import Product

# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('cart')
#         if cart is None:
#             cart = self.session['cart'] = {}
#         self.cart = cart

#     def add(self, product):
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
#         else:
#             self.cart[product_id]['quantity'] += 1  # increment quantity if already added

#         self.session.modified = True

#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())

#     def get_prods(self):
#         product_ids = [int(id) for id in self.cart.keys()]
#         return Product.objects.filter(id__in=product_ids)

#     def get_total_price(self):
#         return sum(float(item['price']) * item['quantity'] for item in self.cart.values())




# from store.models import Product

# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('cart')
#         if cart is None:
#           cart = self.session['cart'] = {}

#         self.cart = cart

#     def add(self, product):
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
#             self.session.modified = True


#     def __len__(self):
#         return len(self.cart) if isinstance(self.cart, dict) else 0

#     def get_prods(self):
#         product_ids = [int(id) for id in self.cart.keys()] if self.cart else []
#         products = Product.objects.filter(id__in=product_ids)
#         return products

        
          