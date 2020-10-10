from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderListSerializer, OrderCheckoutSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.select_related('cart').all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('order_id', 'cart', 'status')

    action_serializers = {
        'list': OrderListSerializer,
        'create': OrderCreateSerializer
    }

    def list(self, request, *args, **kwargs):
        """
        Retrieve Orders
        """
        queryset = Order.objects.select_related('cart').all()
        serializer = OrderListSerializer(queryset, many=True).data
        return Response(serializer)

    def get_permissions(self):
        """
        Block everyone except admin user to create/delete/etc Orders
        Orders can only be cancelled or paid
        """
        if self.action in ['create', 'list']:
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(OrderViewSet, self).get_serializer_class()


class OrderCheckoutViewSet(ModelViewSet):
    serializer_class = OrderCheckoutSerializer
    queryset = Order.objects.select_related('cart').all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('order_id', 'cart', 'status')

    def get_permissions(self):
        """
        Block everyone except admin user to create/delete/etc Orders
        Orders can only be cancelled or paid
        """
        if self.action in ['update']:
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super(self.__class__, self).get_permissions()
