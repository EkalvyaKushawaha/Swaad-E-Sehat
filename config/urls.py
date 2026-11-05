from orders.admin_views import admin_dashboard, update_status
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', admin_dashboard, name='cafe_admin_dashboard'),
    path('dashboard/status/<int:order_id>/<str:new_status>/', update_status, name='update_order_status'),

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('menu/', include('menu.urls')),
    path('tables/', include('tables.urls')),
    path('orders/', include('orders.urls')),
    path('delivery/', include('delivery.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
