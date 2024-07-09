from decimal import Decimal

from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Avg, Sum, F
from django.utils import timezone
from myauth.models import CustomUser


def product_preview_directory_path(instance: "MenuItem", filename: str) -> str:
    """
    Generate the directory path for dish preview images.
    Args:
        instance (MenuItem): The dish instance.
        filename (str): The original filename of the uploaded image.
    Returns:
        str: The directory path where the image will be stored.
    """
    return "menu_item/menu_item_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def category_preview_directory_path(instance: "Category", filename: str) -> str:
    """
    Generate the directory path for category images.
    Args:
        instance (Category): The category instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The directory path where the image will be stored.
    """
    return "category/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Category(models.Model):
    """
    Represents a category of dishes in the restaurant.
    Attributes:
        name (str): The name of the category.
        description (str): A brief description of the category.
        image (ImageField): An image representing the category.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=category_preview_directory_path, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag that can be associated with dishes.
    Attributes:
        name (str): The name of the tag.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Represents a dish in the restaurant menu.
    Attributes:
        name (str): The name of the dish.
        description (str): A brief description of the dish.
        price (DecimalField): The price of the dish.
        category (ForeignKey): The category to which the dish belongs.
        discount (int): The discount on the dish (percentage).
        archived (bool): Indicates whether the dish is archived.
        preview (ImageField): A preview image of the dish.
        available (bool): Indicates whether the dish is available.
        tags (ManyToManyField): Tags associated with the dish.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Dish price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.SmallIntegerField(default=0)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        else:
            return self.description[:50] + '...'

    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     item = form.instance
    #     tags = item.tags.all()
    #     for tag_name in form.cleaned_data['tags']:
    #         tag, created = Tag.objects.get_or_create(name=tag_name)
    #         if tag not in tags:
    #             item.tags.add(tag)


class Order(models.Model):
    status_choice = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('payment', 'payment'),
        ('archived', 'Archived'),
    ]
    payment = [
        ('cash', 'cash'),
        ('card', 'card'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(MenuItem, through='Basket')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=status_choice, default='active')
    payment_type = models.CharField(max_length=20, choices=payment)

    # address = models.TextField()

    def calculate_total_amount(self):
        total_amount = self.items.aggregate(total=Sum(F('price') - F('discount') * F('basket__quantity'), output_field=models.DecimalField()))['total']
        self.total_amount = total_amount
        return total_amount or Decimal('0.00')


class Basket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

