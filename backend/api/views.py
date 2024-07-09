from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from menu.models import (MenuItem,
                         Category,
                         Tag)
from rest_framework.views import APIView
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import MenuItemSerializer, TagSerializer


class TagView(APIView):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuListView(ListAPIView):

    queryset = MenuItem.objects.filter(archived=False, available=True)
    serializer_class = MenuItemSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]

    def list(self, request, *args, **kwargs):
        category = request.data.get("category", None)
        queryset = MenuItem.objects.all()
        if category:
            category_instance = Category.objects.get(name=category)
            queryset = queryset.filter(category=category_instance)

        serialized_items = self.get_serializer(queryset, many=True).data
        data = {
            'items': serialized_items,
        }
        return Response(data, status=status.HTTP_200_OK)


class MenuItemDetailView(RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


