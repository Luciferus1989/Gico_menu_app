from rest_framework import serializers
from menu.models import (MenuItem,
                         Tag,
                         Category,)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class MenuItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

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
