from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin-honeypot')),
    path('adminlogin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('store/', include('store.urls', namespace='store')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('orders/', include('orders.urls', namespace='orders')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)