from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Client(models.Model):
	name=models.CharField(max_length=30)
	email=models.CharField(max_length=30)
	phone=models.CharField(max_length=16, default='xxxxxxxx')
	password=models.CharField(max_length=16)
	gender=models.CharField(max_length=1,default='M')
	birthday=models.DateField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return self.name


class Member(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE , default=None)  
    Mname = models.CharField(max_length=30)
    Memail = models.EmailField(max_length=254)
    Mphone = models.CharField(max_length=15)
    membership_type = models.CharField(max_length=20)

    def __str__(self):
        return self.Mname

class Sport(models.Model):
	SportName=models.CharField(max_length=30)
	nbClients=models.IntegerField()
	def __str__ (self):
		return self.SportName

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    reserved_sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=None)
    reservation_date = models.DateField(null=True, blank=True)  # Making the date field not required
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coach = models.CharField(max_length=100, null=True, blank=True)
    
    
    DATE_OPTIONS = [
        ('year', 'Year'),
        ('month', 'Month'),
        ('week', 'Week'),
    ]
    date_option = models.CharField(max_length=5, choices=DATE_OPTIONS, blank=True)  
    
    def __str__(self):
        return f"{self.client}-{self.reserved_sport}"

class Product(models.Model):
    pname = models.CharField(max_length=30)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='item_images')
    price = models.DecimalField(decimal_places=2, max_digits=10000, default=0.00)
    
    def __str__(self):
        return self.pname

class CartItem(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE ,default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.client}-{self.product}"

def total_price(self):
        return self.product.price * self.quantity



