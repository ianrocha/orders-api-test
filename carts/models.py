from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from clients.models import Client
from products.models import Product


class CartQuerySet(models.query.QuerySet):
    def cart_active(self):
        return self.filter(activate=1)


class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)

    def cart_active(self):
        return self.get_queryset().cart_active()


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    activate = models.BooleanField(default=True)
    total_cart_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    objects = CartManager()

    def __str__(self):
        return f"Cart: {self.cart_id}, Client: {self.client.name}, CartTotal: {self.total_cart_price}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_product_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return f'Cart: {self.cart}, Product: {self.product}, Quantity: {self.quantity}'


def pre_save_create_cart_item(sender, instance, *args, **kwargs):
    """
    Calculate the total price of product -> product price * quantity
    """
    if instance:
        instance.total_product_price = instance.product.price * instance.quantity


pre_save.connect(pre_save_create_cart_item, sender=CartItem)


def post_save_cart_item(sender, instance, *args, **kwargs):
    """
    Calculate the total price of cart -> product price * quantity
    """
    if instance:
        instance.cart.total_cart_price += instance.total_product_price
        instance.cart.save()


post_save.connect(post_save_cart_item, sender=CartItem)


def post_delete_cart_item(sender, instance, *args, **kwargs):
    """
    Calculate the total price of cart -> product price * quantity
    """
    if instance:
        instance.cart.total_cart_price -= instance.total_product_price
        instance.cart.save()


post_delete.connect(post_delete_cart_item, sender=CartItem)
