from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'Thanh toán qua VNPay'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Chờ xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # For VNPay transaction ID
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order {self.id} - {self.full_name}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.shipping_fee
    
    def get_items_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_cost(self):
        return self.price * self.quantity


class VNPayTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ thanh toán'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('cancelled', 'Đã hủy'),
    )
    
    order = models.ForeignKey(Order, related_name='vnpay_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    vnp_txn_ref = models.CharField(max_length=100, unique=True)  # VNPay transaction reference
    vnp_transaction_no = models.CharField(max_length=100, blank=True, null=True)  # VNPay transaction number
    vnp_response_code = models.CharField(max_length=10, blank=True, null=True)
    vnp_bank_code = models.CharField(max_length=20, blank=True, null=True)
    vnp_bank_tran_no = models.CharField(max_length=255, blank=True, null=True)
    vnp_card_type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'VNPay Transaction {self.vnp_txn_ref}'
