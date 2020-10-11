"""orderapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

from carts.viewset import CartViewSet, CartItemViewSet
from clients.viewset import ClientViewSet
from orders.viewset import OrderViewSet, OrderCheckoutViewSet
from products.viewset import ProductViewSet


schema_view = get_schema_view(title='OrderApi',
                              description='OrderAPI',
                              version='1.0.0')

router = DefaultRouter()
router.register(r'client', ClientViewSet, basename='ClientViewSet')
router.register(r'product', ProductViewSet, basename='ProductViewSet')
router.register(r'order', OrderViewSet, basename='OrderViewSet')
router.register(r'order_checkout', OrderCheckoutViewSet, basename='OrderCheckoutViewSet')
router.register(r'cart', CartViewSet, basename='CartViewSet')
router.register(r'cart_items', CartItemViewSet, basename='CartItemViewSet')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', schema_view)
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
