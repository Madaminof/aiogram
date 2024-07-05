from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Menyu(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    class Meta:
        db_table = 'menu'


    def __str__(self):
        return f"{self.name}-{self.price}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Menyu, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Menyu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Kontakt(models.Model):
    addres = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15)
    network = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'kontakt'

    def __str__(self):
        return f"Kontakt: {self.addres}"







