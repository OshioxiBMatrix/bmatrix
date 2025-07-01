from django.contrib import admin
from .models import Order, OrderItem, VNPayTransaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

class VNPayTransactionInline(admin.TabularInline):
    model = VNPayTransaction
    readonly_fields = ['vnp_txn_ref', 'vnp_transaction_no', 'vnp_response_code', 'vnp_bank_code', 'vnp_bank_tran_no', 'vnp_card_type', 'status', 'created_at', 'updated_at']
    extra = 0
    can_delete = False
    max_num = 0  # Don't allow adding new transactions from admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'paid', 'payment_method', 'status', 'created_at']
    list_filter = ['paid', 'payment_method', 'status', 'created_at']
    search_fields = ['id', 'full_name', 'email', 'phone']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline, VNPayTransactionInline]
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Thông tin khách hàng', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Địa chỉ giao hàng', {
            'fields': ('province', 'district', 'ward', 'address', 'note')
        }),
        ('Thanh toán', {
            'fields': ('payment_method', 'paid', 'payment_id', 'shipping_fee')
        }),
    )

@admin.register(VNPayTransaction)
class VNPayTransactionAdmin(admin.ModelAdmin):
    list_display = ['vnp_txn_ref', 'order', 'amount', 'status', 'vnp_response_code', 'created_at']
    list_filter = ['status', 'created_at', 'vnp_bank_code']
    search_fields = ['vnp_txn_ref', 'vnp_transaction_no', 'order__id', 'order__full_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['order', 'amount', 'vnp_txn_ref', 'vnp_transaction_no', 'vnp_response_code', 'vnp_bank_code', 'vnp_bank_tran_no', 'vnp_card_type', 'created_at', 'updated_at']
    fieldsets = (
        ('Thông tin giao dịch', {
            'fields': ('order', 'amount', 'status', 'created_at', 'updated_at')
        }),
        ('Thông tin VNPay', {
            'fields': ('vnp_txn_ref', 'vnp_transaction_no', 'vnp_response_code', 'vnp_bank_code', 'vnp_bank_tran_no', 'vnp_card_type')
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Don't allow adding transactions manually
