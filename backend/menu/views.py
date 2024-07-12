from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import (MenuItem,
                     Category,
                     Tag,
                     Order,
                     Basket)
from rest_framework.views import APIView
from .serializers import MenuItemSerializer, TagSerializer, BasketItemSerializer, OrderDetailSerializer
from django.shortcuts import get_object_or_404


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

class BasketAPIView(APIView):
    serializer_class = BasketItemSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer_identifier = request.user.id
        else:
            session_key = request.session.session_key
            custom_user = CustomUser.objects.filter(session_key=session_key).first()
            customer_identifier = custom_user.id
        order = Order.objects.filter(customer=customer_identifier, status='active').first()
        basket_items = Basket.objects.filter(order=order)
        serializer = self.serializer_class(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        item = MenuItem.objects.get(pk=request.data.get('id', 0))
        count = int(request.data.get('count', 0))
        if request.user.is_authenticated:
            customer_identifier = request.user
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            customer_identifier, created = CustomUser.objects.get_or_create(session_key=session_key)

        order, created = Order.objects.get_or_create(customer=customer_identifier, status='active', total_amount=0)
        order_list, created = Basket.objects.get_or_create(order=order, item=item)
        sale_price = item.price - item.discount
        order_list.sale_price = sale_price
        order_list.quantity += count
        order_list.save()

        serializer = self.serializer_class(order_list, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        data = request.data
        item_id = data['id']
        count = data['count']
        if request.user.is_authenticated:
            customer_identifier = request.user
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            customer_identifier, created = CustomUser.objects.get_or_create(session_key=session_key)

        order = Order.objects.filter(customer=customer_identifier, status='active').first()
        basket_item = Basket.objects.filter(order=order, item_id=item_id).first()
        if count < basket_item.quantity:
            basket_item.quantity -= count
            basket_item.save()
        else:
            basket_item.delete()
            remaining_items = Basket.objects.filter(order=order).exists()
            if not remaining_items:
                order.delete()
                serializer = BasketItemSerializer([], many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        updated_basket_items = Basket.objects.filter(order=order)

        serializer = BasketItemSerializer(updated_basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPIView(APIView):

    def get(self, request, *args, **kwargs):
        customer_identifier = request.user.id
        orders = Order.objects.filter(customer=customer_identifier)
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        customer_identifier = request.user.id
        order = Order.objects.filter(customer=customer_identifier, status='active').first()
        if order:
            order.total_amount = order.calculate_total_amount()
            order.status = 'pending'
            order.save()
            response_data = {'orderId': order.id}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(self.queryset, id=kwargs[self.lookup_field])
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(self.queryset, id=kwargs[self.lookup_field])
        data = request.data
        order.customer.update_name(data.get('fullName', order.customer.get_fullName()))
        order.payment_type = data.get('paymentType', order.payment_type)
        order.city = data.get('city', order.city)
        order.address = data.get('address', order.address)
        order.delivery_type = data.get('deliveryType', order.delivery_type)
        total_amount = order.total_amount
        order.total_amount = total_amount
        order.status = 'payment'
        order.save()
        print(order.payment_type)

        return Response({'orderId': order.id})
