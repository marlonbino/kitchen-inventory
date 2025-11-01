from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet,
    StockMovementViewSet,
    RequisitionViewSet,
    LowStockView,
    DashboardStatsView
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'stock-movements', StockMovementViewSet, basename='stockmovement')
router.register(r'requisitions', RequisitionViewSet, basename='requisition')

app_name = 'inventory'
urlpatterns = [
    # Router URLs for viewsets
    path('', include(router.urls)),
    
    # Custom endpoints
    path('low-stock/', LowStockView.as_view(), name='low-stock'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
