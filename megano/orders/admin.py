from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "profile",
        "totalCost",
        "status",
        "paymentType",
        "deliveryType",
        "city",
        "createdAt",
    ]
    list_filter = [
        "profile",
        "status_id",
        "paymentType_id",
        "deliveryType_id",
        "city",
        "createdAt",
    ]
    search_fields = ["profile"]

    def get_queryset(self, request):
        return Order.objects.select_related('profile')\
            .select_related('status_id')\
            .select_related('deliveryType_id')\
            .select_related('paymentType_id')\
