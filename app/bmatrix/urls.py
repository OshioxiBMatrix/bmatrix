from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('shop.urls', namespace='shop')),  # Make shop the default app
    path('terms-of-service/', TemplateView.as_view(template_name='terms_of_service.html'), name='terms_of_service'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

