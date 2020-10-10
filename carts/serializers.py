from rest_framework import serializers

from carts.models import Cart, CartItem
from clients.serializers import ClientInCartSerializer
from products.models import Product
from products.serializers import ProductSerializer


class CartCreateSerializer(serializers.ModelSerializer):
    """
    Create a new Cart
    """
    class Meta:
        model = Cart
        fields = ('client', )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'total_product_price')


class CartListSerializer(serializers.ModelSerializer):
    """
    Retrieve all Carts and the CartItems
    """
    cart_items = CartItemSerializer(many=True, read_only=True)
    client = ClientInCartSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('cart_id', 'client', 'cart_items', 'total_cart_price', 'activate')


class CartItemCreateSerializer(serializers.ModelSerializer):
    """
    Create new CartItem on Cart
    """
    cart = CartCreateSerializer(write_only=True, required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'cart')

    def create(self, validated_data):
        """
        Add/Update CartItem to a Cart or create a new Cart if there's no Active Cart
        """
        client = validated_data.pop('cart', {}).pop('client')
        cart_obj, created = Cart.objects.get_or_create(client=client, activate=True)
        if created:
            validated_data['cart_id'] = cart_obj.cart_id
            cart_item_obj = CartItem.objects.create(**validated_data)
        else:
            validated_data['cart_id'] = cart_obj.cart_id
            cart_item_objs = CartItem.objects.filter(cart=cart_obj.cart_id,
                                                     product__product_id=validated_data['product'].product_id)
            if len(cart_item_objs) > 0:
                cart_item_obj = cart_item_objs[0]
                cart_item_obj.quantity = validated_data['quantity']
                cart_item_obj.save()
            else:
                cart_item_obj = CartItem.objects.create(**validated_data)
        return cart_item_obj


class CartItemGenericListSerializer(serializers.ModelSerializer):
    """
    Retrieve all CartItems
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ("cart", "product", "quantity", "total_product_price")
