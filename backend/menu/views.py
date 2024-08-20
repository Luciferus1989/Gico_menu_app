from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import (MenuItem,
                     Category,
                     Tag,
                     Order,
                     Basket)
from rest_framework.views import APIView
from .serializers import MenuItemSerializer, TagSerializer, BasketItemSerializer, OrderDetailSerializer, CategorySerializer, MenuItemManagerSerializer
from django.shortcuts import get_object_or_404
from myauth.models import CustomUser


class TagView(APIView):
    """
    API View to retrieve all tags.

    Methods:
    - get: Retrieve all tags from the database and return them serialized.
    """
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuListView(ListAPIView):
    """
    API View to list all available menu items.

    Attributes:
    - queryset: Queryset to retrieve all non-archived, available menu items.
    - serializer_class: Serializer to use for menu items.

    Methods:
    - list: Retrieve all menu items, optionally filtered by category.
    """
    serializer_class = MenuItemSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]

    def list(self, request, *args, **kwargs):
        category = request.data.get("category", None)
        queryset = MenuItem.objects.filter(archived=False, available=True)
        if category:
            category_instance = Category.objects.get(name=category)
            queryset = queryset.filter(category=category_instance)

        serialized_items = self.get_serializer(queryset, many=True).data
        data = {
            'items': serialized_items,
        }
        return Response(data, status=status.HTTP_200_OK)


class MenuItemDetailView(RetrieveAPIView):
    """
    API View to retrieve a single menu item by its ID.

    Attributes:
    - queryset: Queryset to retrieve all menu items.
    - serializer_class: Serializer to use for menu items.
    - lookup_field: Field to use for looking up the menu item.

    Methods:
    - retrieve: Retrieve and return the menu item specified by the ID.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BasketAPIView(APIView):
    """
    API View to manage the user's basket.

    Methods:
    - get: Retrieve all items in the user's basket.
    - post: Add items to the user's basket.
    - delete: Remove items from the user's basket.
    """
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
    """
    API View to manage user orders.

    Methods:
    - get: Retrieve all orders for the authenticated user.
    - post: Finalize the active order for the authenticated user.
    """
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
    """
    API View to retrieve and update a single order by its ID.

    Attributes:
    - queryset: Queryset to retrieve all orders.
    - serializer_class: Serializer to use for orders.
    - lookup_field: Field to use for looking up the order.

    Methods:
    - get: Retrieve and return the order specified by the ID.
    - post: Update the specified order with new details.
    """
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


class CategoryApiView(APIView):
    """
    API view to retrieve the list of all categories.

    Methods:
    -------
        Handles GET requests and returns a list of all categories in JSON format.
    """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemView(APIView):
    """
    API view to manage menu items.

    Methods:
    -------
    post(request):
        Handles POST requests to create a new menu item.

    put(request, pk):
        Handles PUT requests to update an existing menu item by its primary key (pk).

    delete(request, *args, **kwargs):
        Handles DELETE requests to archive a menu item based on its ID.
    """
    def post(self, request):
        """
        Creates a new menu item.

        Parameters:
        ----------
        request : Request
            The request object containing the data for the new menu item.

        Returns:
        -------
        Response
            A JSON response containing the created menu item data and a status code 201 if successful,
            or the validation errors and a status code 400 if not.
        """
        serializer = MenuItemManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Updates an existing menu item.

        Parameters:
        ----------
        request : Request
            The request object containing the updated data for the menu item.
        pk : int
            The primary key of the menu item to be updated.

        Returns:
        -------
        Response
            A JSON response containing the updated menu item data and a status code 200 if successful,
            or a 404 status if the menu item is not found, or validation errors and a status code 400 if not.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Archives a menu item by setting its 'archived' field to True.

        Parameters:
        ----------
        request : Request
            The request object containing the ID of the menu item to be archived.

        Returns:
        -------
        Response
            A status code 204 if the operation is successful, or 404 if the menu item is not found.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data
        item_id = data['id']
        try:
            item = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.archived = True
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

