from rest_framework import serializers
from .models import (MenuItem,
                     Tag,
                     Category,
                     Basket,
                     Order,)
from decimal import Decimal

from myauth.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id',
                  'name',
                  'price',
                  'discount',
                  'preview',
                  'category',
                  'tags',
                  ]

    def get_category(self, obj):
        return obj.category.name


class MenuItemManagerSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = MenuItem
        fields = ['id',
                  'name',
                  'price',
                  'discount',
                  'preview',
                  'category',
                  'tags',
                  ]

    def get_category(self, obj):
        return obj.category.name


class BasketItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer()
    quantity = serializers.IntegerField(source='quantity')

    class Meta:
        model = Basket
        fields = ['item', 'quantity']

    def to_representation(self, instance):
        item_representation = MenuItemSerializer(instance.item).data
        sale_price = instance.item.price * (1 - Decimal(instance.item.discount) / 100)
        return {
            'id': item_representation['id'],
            'category': item_representation['category'],
            'price': sale_price,
            'count': instance.quantity,
            'date': item_representation['date'],
            'title': item_representation['title'],
            'description': item_representation['description'],
            'freeDelivery': item_representation['free_delivery'],
            'images': item_representation['images'],
            'tags': item_representation['tags'],
            'reviews': item_representation['reviews'],
            'rating': item_representation['rating'],
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    products = BasketItemSerializer(many=True, read_only=True, source='basket_set')
    deliveryType = serializers.SerializerMethodField()
    paymentType = serializers.CharField(source='payment_type')
    totalCost = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_amount')

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'customer', 'deliveryType', 'paymentType',
                  'status', 'city', 'address', 'products', 'totalCost']

    def get_deliveryType(self, obj):
        has_paid_delivery = any(item.free_delivery is False for item in obj.items.all())
        return 'free' if not has_paid_delivery else 'paid'

    def to_representation(self, instance):
        formatted_data = {
            'id': instance.id,
            'createdAt': instance.created_at.strftime('%Y-%m-%d %H:%M'),
            'fullName': instance.customer.get_fullName(),
            'email': instance.customer.email,
            'phone': instance.customer.phone,
            'deliveryType': self.get_deliveryType(instance),
            'paymentType': instance.payment_type,
            'totalCost': instance.total_amount,
            'status': instance.status,
            'city': instance.city,
            'address': instance.address,
            'products': BasketItemSerializer(instance.basket_set.all(), many=True).data,
        }

        return formatted_data