from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import request
from .views import MenuListView, MenuItemDetailView, TagView

app_name = 'api'

urlpatterns = [
    path('menu/', MenuListView.as_view(), name='menu_api'),
    path('menu/<int:id>/', MenuItemDetailView.as_view(), name='menu-detail'),
    path('tags/', TagView.as_view(), name='tags'),
]
