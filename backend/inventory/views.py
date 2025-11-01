from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db.models import F, Sum
from .models import Item, StockMovement, Requisition
from .serializers import (
    ItemSerializer,
    StockMovementSerializer,
    RequisitionSerializer,
    LowStockItemSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class with page size of 20."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item model with full CRUD operations.
    Includes filtering, search, and ordering capabilities.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'unit']
    search_fields = ['name']
    ordering_fields = ['name', 'current_stock', 'min_stock_level']
    ordering = ['name']


class StockMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StockMovement model with full CRUD operations.
    Includes filtering and automatic stock validation on create.
    """
    queryset = StockMovement.objects.select_related('item').all()
    serializer_class = StockMovementSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['movement_type', 'item']
    ordering_fields = ['date', 'quantity']
    ordering = ['-date']

    def create(self, request, *args, **kwargs):
        """
        Override create to ensure stock validation happens.
        The serializer's validate method will handle stock validation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RequisitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Requisition model with full CRUD operations.
    Includes filtering and custom approve/reject actions.
    """
    queryset = Requisition.objects.select_related('item').all()
    serializer_class = RequisitionSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'item']
    ordering_fields = ['date_requested', 'date_processed']
    ordering = ['-date_requested']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Custom action to approve a requisition.
        Updates status to 'approved' and sets date_processed.
        """
        try:
            requisition = self.get_object()
            
            if requisition.status != 'pending':
                return Response(
                    {'error': f'Requisition is already {requisition.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            requisition.status = 'approved'
            requisition.date_processed = timezone.now()
            requisition.save()
            
            serializer = self.get_serializer(requisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Custom action to reject a requisition.
        Updates status to 'rejected' and sets date_processed.
        """
        try:
            requisition = self.get_object()
            
            if requisition.status != 'pending':
                return Response(
                    {'error': f'Requisition is already {requisition.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            requisition.status = 'rejected'
            requisition.date_processed = timezone.now()
            requisition.save()
            
            serializer = self.get_serializer(requisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LowStockView(APIView):
    """
    Custom APIView to get all items with low stock levels.
    Returns items where current_stock < min_stock_level.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        GET endpoint at /api/low-stock/
        Returns all items where current_stock < min_stock_level.
        """
        try:
            low_stock_items = Item.objects.filter(
                current_stock__lt=F('min_stock_level')
            )
            
            serializer = LowStockItemSerializer(low_stock_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardStatsView(APIView):
    """
    Custom APIView to get dashboard statistics.
    Returns aggregated data for the inventory dashboard.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        GET endpoint at /api/dashboard-stats/
        Returns JSON with:
        - total_items: count of all items
        - low_stock_count: count of items below min level
        - pending_requisitions: count of pending requisitions
        - recent_movements: last 5 stock movements
        - total_stock_value: sum of all current_stock
        """
        try:
            # Total items count
            total_items = Item.objects.count()
            
            # Low stock count
            low_stock_count = Item.objects.filter(
                current_stock__lt=F('min_stock_level')
            ).count()
            
            # Pending requisitions count
            pending_requisitions = Requisition.objects.filter(
                status='pending'
            ).count()
            
            # Recent movements (last 5)
            recent_movements = StockMovement.objects.select_related('item').order_by('-date')[:5]
            recent_movements_serializer = StockMovementSerializer(recent_movements, many=True)
            
            # Total stock value (sum of all current_stock)
            total_stock_value = Item.objects.aggregate(
                total=Sum('current_stock')
            )['total'] or 0
            
            stats = {
                'total_items': total_items,
                'low_stock_count': low_stock_count,
                'pending_requisitions': pending_requisitions,
                'recent_movements': recent_movements_serializer.data,
                'total_stock_value': total_stock_value
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
