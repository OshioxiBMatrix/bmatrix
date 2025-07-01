from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('vnpay/payment/<int:order_id>/', views.vnpay_payment, name='vnpay_payment'),
    path('vnpay/callback/', views.vnpay_callback, name='vnpay_callback'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # API endpoints for address selection
    path('api/districts/<int:province_id>/', views.get_districts_api, name='get_districts_api'),
    path('api/wards/<int:district_id>/', views.get_wards_api, name='get_wards_api'),
]
