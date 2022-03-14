from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


#customer model
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.first_name

#promotion model
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    
    def __str__(self) -> str:
        return self.description

#collection model
class Collection(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title

# products model
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField (default ='-')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, 
                                decimal_places=2, 
                                validators=[MinValueValidator(0)]
                                )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ForeignKey(Promotion, on_delete=models.PROTECT, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
        

        
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    #products = models.ManyToManyField(OrderItem)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    street = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address