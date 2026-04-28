from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/', include('orders.urls')),
    
    # UI endpoints
    path('ui/users/', include('users.urls_ui')),
    path('ui/products/', include('products.urls_ui')),
    path('ui/orders/', include('orders.urls_ui')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
