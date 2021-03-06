from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
