from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "goods_title",
        "price",
        "amount",
        "get_total_price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "created",
        "get_total_price",
    )
    list_filter = ("status", "created")
    search_fields = ("user",)
    readonly_fields = ("created", "get_total_price")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "goods_title",
        "price",
        "amount",
        "get_total_price",
    )
    list_filter = ("order",)
    search_fields = ("goods_title",)
