from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet
from .views import ConfirmOrderDispatchView
from django.urls import path


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls

urlpatterns += [
    path('confirm-order/<int:order_id>/', ConfirmOrderDispatchView.as_view(), name='confirm_order_dispatch'),
]