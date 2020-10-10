from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart, CartItem
from carts.serializers import CartListSerializer, CartItemCreateSerializer, \
    CartItemGenericListSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartListSerializer
    queryset = Cart.objects.cart_active()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = '__all__'

    def get_permissions(self):
        """
        Block everyone except admin user to create/delete/etc Carts
        Carts are automatically created when an item is selected
        """
        if self.action in ['list']:
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a Join of Cart with CartItems
        """
        queryset = Cart.objects.cart_active()
        serializer = CartListSerializer(queryset, many=True).data
        if serializer:
            return Response(serializer)
        return Response({"message": "No active carts to show"})


class CartItemViewSet(ModelViewSet):
    """
    View for CartItem, it can retrieve or create objects
    """
    serializer_class = CartItemCreateSerializer
    queryset = CartItem.objects.all()
    filter_backends = (DjangoFilterBackend,)

    action_serializers = {
        'list': CartItemGenericListSerializer,
        'create': CartItemCreateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(CartItemViewSet, self).get_serializer_class()
