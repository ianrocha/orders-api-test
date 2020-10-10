import random
import string

from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled')
)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """
    :return: A new random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator():
    """
    :return: A new random order id
    """
    order_new_id = random_string_generator()
    return order_new_id


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


def post_save_create_order_id(sender, instance, *args, **kwargs):
    """
    Close cart
    """
    if instance.status != 'created':
        instance.cart.activate = False
        instance.cart.save()


post_save.connect(post_save_create_order_id, sender=Order)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    """
    Obtain the order id before saving it
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator()


pre_save.connect(pre_save_create_order_id, sender=Order)
