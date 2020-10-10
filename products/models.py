from django.db import models


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)

    def __str__(self):
        return self.name
