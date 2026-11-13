from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


admin.site.register(Cart)
admin.site.register(CartItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish_name', 'unit_price', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('user', 'created_at', 'total')
    inlines = [OrderItemInline]