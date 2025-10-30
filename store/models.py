from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


# Create your models here.

# Categories Name
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category' # to change the name in admin panel
        verbose_name_plural = 'Categories' # to change the plural name in admin panel

# Customer detials
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
# Products details

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

# Order details
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

    