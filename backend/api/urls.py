from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import request
from menu.views import MenuListView, MenuItemDetailView, TagView, BasketAPIView, OrderAPIView, OrderDetailAPIView, CategoryApiView, ItemView
from myauth.views import LoginApiView, LogoutApiView, RegisterApiView, ProfileAPIView
app_name = 'api'

urlpatterns = [
    path('menu/', MenuListView.as_view(), name='menu_api'),
    path('menu/<int:id>/', MenuItemDetailView.as_view(), name='menu-detail'),
    path('item/', ItemView.as_view(), name='dish'),
    path('tags/', TagView.as_view(), name='tags'),
    path('category/', CategoryApiView.as_view(), name='category'),
    path('basket/', BasketAPIView.as_view(), name='basket'), # to see what is ordered
    path('basket/<int:id>/', BasketAPIView.as_view(), name='basket_id'), # use id of item and put in basket
    path('order/', OrderAPIView.as_view(), name='basket_id'), # user can get the list of his orders
    path('order/<int:id>/', OrderAPIView.as_view(), name='basket_id'), # user can see details of concrete order
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='login'),
]
