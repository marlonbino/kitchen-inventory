from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ItemViewSet,
    StockMovementViewSet,
    RequisitionViewSet,
    LowStockView,
    DashboardStatsView
)
from .auth_views import register, login_view, logout_view, user_info, admin_create_user, admin_list_users, admin_delete_user

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'stock-movements', StockMovementViewSet, basename='stockmovement')
router.register(r'requisitions', RequisitionViewSet, basename='requisition')

app_name = 'inventory'
urlpatterns = [
    # Router URLs for viewsets
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/register/', register, name='register'),  # Disabled for security
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', user_info, name='user-info'),
    
    # Admin-only user management endpoints
    path('admin/users/', admin_list_users, name='admin-list-users'),
    path('admin/users/create/', admin_create_user, name='admin-create-user'),
    path('admin/users/<int:user_id>/delete/', admin_delete_user, name='admin-delete-user'),
    
    # Custom endpoints
    path('low-stock/', LowStockView.as_view(), name='low-stock'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
