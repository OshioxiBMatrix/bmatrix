from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import custom_page_not_found
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('shop.urls', namespace='shop')),  # Make shop the default app
    path('terms-of-service/', TemplateView.as_view(template_name='terms_of_service.html'), name='terms_of_service'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('certification/', TemplateView.as_view(template_name='certification.html'), name='certification'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('team/', TemplateView.as_view(template_name='team.html'), name='team'),
    path('popup-banner/', TemplateView.as_view(template_name='popup_banner.html'), name='popup_banner'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('returns-policy/', TemplateView.as_view(template_name='returns_policy.html'), name='returns_policy'),
    path('shipping-policy/', TemplateView.as_view(template_name='shipping_policy.html'), name='shipping_policy'),
    
    # Add explicit media URL pattern that works in both DEBUG and production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
    # Catch-all pattern - phải đặt ở cuối cùng
    re_path(r'^.*$', lambda request: custom_page_not_found(request, None)),
]

# Custom 404 error handler
handler404 = 'bmatrix.views.custom_page_not_found'

# These are only for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

