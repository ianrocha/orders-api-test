from rest_framework import serializers

from carts.models import Cart
from carts.serializers import CartListSerializer
from orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.filter(activate=True))

    class Meta:
        model = Order
        fields = ('cart',)


class OrderListSerializer(serializers.ModelSerializer):
    cart = CartListSerializer()

    class Meta:
        model = Order
        fields = ('order_id', 'cart', 'status')


class OrderCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'status')

    def update(self, instance, validated_data):
        new_status = validated_data.pop('status')
        instance.status = new_status
        instance.save()
        return instance
