from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'frontend'

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html")),
]
