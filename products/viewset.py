from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from products.serializers import ProductSerializer
from products.models import Product


class ProductViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'description', 'price')

