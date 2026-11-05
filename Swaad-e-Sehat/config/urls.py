"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('admin/', admin.site.urls),

# Home page and core pages
path('', include('core.urls')),

# Orders and cart pages
path('', include('orders.urls')),

# Food management pages
path('food/', include('menu.urls')),

]

if settings.DEBUG:
    urlpatterns += static(
settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT
)