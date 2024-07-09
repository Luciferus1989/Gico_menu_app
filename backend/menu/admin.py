from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from .models import MenuItem, Order, Basket, Category, Tag
from .forms import MenuItemForm


class BasketInline(admin.TabularInline):
    model = Basket
    extra = 1


class ItemTagsInline(admin.TabularInline):
    model = MenuItem.tags.through
    extra = 1


@admin.action(description='Archive selected menu items')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchived selected menu items')
def remark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.action(description='Set discount 10 percent')
def set_discount_10(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=10)


@admin.action(description='Set discount 5 percent')
def set_discount_5(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=5)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'description_short', 'category', 'available', 'archived')
    ordering = ('name',)
    search_fields = ('name',)
    form_class = MenuItemForm
    inlines = [
        ItemTagsInline,
        BasketInline,
    ]
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'category', 'available')
        }),
        ('Pricing', {
            'fields': ('price', 'discount'),
            'description': 'The price is specified in $AUD',
        }),
        ('Availability', {
            'fields': ('archived',)
        }),
        ('Pictures', {
            'fields': ('preview',)
        })
    ]
    actions = [
        mark_archived,
        remark_archived,
        set_discount_5,
        set_discount_10,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.action(description='Archive selected orders')
def mark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='archived')


@admin.action(description='Unarchive selected orders')
def remark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'total_amount')
    inlines = [
        BasketInline,
    ]
    actions = [
        mark_archived_order,
        remark_archived_order,
    ]
    readonly_fields = ('created_at', 'user', 'total_amount')
    fieldsets = [
        (None, {
            'fields': ('user', 'created_at', 'total_amount'),
        }),
        ('Order Details', {
            'fields': ('status', 'payment_type'),
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('dishes')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'sale_price')

