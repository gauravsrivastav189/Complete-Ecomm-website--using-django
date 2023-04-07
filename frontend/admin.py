from django.contrib import admin
from .models import Item, Order, OrderItem, Coupon, Payment, BillingAddress, Refund


def change_refund_to_granted(modelAdmin, request, queryset):
    queryset.update(refund_granted=True)

def change_to_delivered(modelAdmin, request, queryset):
    queryset.update(delivered=True, received=True)

class SnippetOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'delivered', 'refund_requested', 'refund_granted', 'billing_address', 'payment', 'coupon']
    list_display_links = ['user', 'billing_address', 'payment', 'coupon']

    actions = [change_refund_to_granted, change_to_delivered]


admin.site.register(Item)
admin.site.register(Order, SnippetOrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(Refund)
