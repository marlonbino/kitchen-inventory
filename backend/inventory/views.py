from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db.models import F, Sum
from .models import Category, Item, StockMovement, Requisition, UserProfile
from .serializers import (
    CategorySerializer,
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


def is_admin(user):
    """Check if user has admin role."""
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role == 'admin'
    except UserProfile.DoesNotExist:
        return False


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model.
    Only admins can manage categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Categories don't need pagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_queryset(self):
        """Everyone can view, but only admins can create/update/delete."""
        from django.db.models import Count
        return Category.objects.annotate(item_count=Count('items'))
    
    def create(self, request, *args, **kwargs):
        """Only admins can create categories."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can create categories.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Only admins can update categories."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can update categories.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete categories."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can delete categories.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item model with full CRUD operations.
    Includes filtering, search, and ordering capabilities.
    """
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'unit']
    search_fields = ['name']
    ordering_fields = ['name', 'current_stock', 'min_stock_level']
    ordering = ['name']
    
    def get_queryset(self):
        """Shared kitchen - all users see all items."""
        return Item.objects.all()
    
    def perform_create(self, serializer):
        """Automatically assign the item creator."""
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Only admins can create items."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can create items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Only admins can update items."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can update items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete items."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can delete items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class StockMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StockMovement model with full CRUD operations.
    Includes filtering and automatic stock validation on create.
    """
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['movement_type', 'item']
    ordering_fields = ['date', 'quantity']
    ordering = ['-date']
    
    def get_queryset(self):
        """Shared kitchen - all users see all movements."""
        return StockMovement.objects.select_related('item').all()

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
    
    def update(self, request, *args, **kwargs):
        """Only admins can update movements."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can update stock movements.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only admins can delete movements."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can delete stock movements.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class RequisitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Requisition model with full CRUD operations.
    Includes filtering and custom approve/reject actions.
    """
    serializer_class = RequisitionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'item']
    ordering_fields = ['date_requested', 'date_processed']
    ordering = ['-date_requested']
    
    def get_queryset(self):
        """Shared kitchen - all users see all requisitions."""
        return Requisition.objects.select_related('item').all()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Custom action to approve a requisition.
        Updates status to 'awaiting_delivery' and sets date_processed.
        Requires money_received_by to indicate who received the money.
        ONLY ADMINS CAN APPROVE.
        """
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {'error': 'Only administrators can approve requisitions.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get money_received_by from request
        money_received_by = request.data.get('money_received_by', '').strip()
        if not money_received_by:
            return Response(
                {'error': 'Please specify who received the money for this purchase.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            requisition = self.get_object()
            
            if requisition.status != 'pending':
                return Response(
                    {'error': 'Only pending requisitions can be approved.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            requisition.status = 'awaiting_delivery'
            requisition.date_processed = timezone.now()
            requisition.approved_by = request.user.username
            requisition.money_received_by = money_received_by
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
        ONLY ADMINS CAN REJECT.
        """
        # Check if user is admin
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can reject requisitions.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
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
    
    @action(detail=True, methods=['post'])
    def assign_delivery(self, request, pk=None):
        """
        Assign delivery to a person when admin receives the items.
        Only admin can assign delivery.
        """
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can assign deliveries.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            requisition = self.get_object()
            
            if requisition.status != 'awaiting_delivery':
                return Response(
                    {'error': f'Can only assign delivery to requisitions awaiting delivery. Current status: {requisition.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            assigned_to = request.data.get('assigned_to', '').strip()
            if not assigned_to:
                return Response(
                    {'error': 'assigned_to field is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            requisition.assigned_to = assigned_to
            requisition.save()
            
            serializer = self.get_serializer(requisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def confirm_received(self, request, pk=None):
        """
        Confirm that items were received.
        Updates status to 'delivered' and creates a stock movement receipt.
        Validates quantity_received <= quantity_requested and requires notes if less.
        """
        try:
            requisition = self.get_object()
            
            if requisition.status != 'awaiting_delivery':
                return Response(
                    {'error': f'Can only confirm receipt for requisitions awaiting delivery. Current status: {requisition.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user is assigned or admin
            received_by = request.data.get('received_by', '').strip() or request.user.username
            if not is_admin(request.user):
                if requisition.assigned_to and requisition.assigned_to.lower() != received_by.lower():
                    return Response(
                        {'error': f'Only {requisition.assigned_to} can confirm this receipt.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Get quantity received (defaults to requested if not provided)
            quantity_received = request.data.get('quantity_received')
            if quantity_received is None:
                quantity_received = requisition.quantity_requested
            else:
                quantity_received = int(quantity_received)
            
            # Validate quantity
            if quantity_received <= 0:
                return Response(
                    {'error': 'Quantity received must be greater than 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if quantity_received > requisition.quantity_requested:
                return Response(
                    {'error': 'Quantity received cannot exceed quantity requested'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check notes requirement
            receipt_notes = request.data.get('receipt_notes', '').strip()
            if quantity_received < requisition.quantity_requested and not receipt_notes:
                return Response(
                    {'error': 'Notes are required when quantity received is less than requested'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update requisition
            requisition.status = 'delivered'
            requisition.received_by = received_by
            requisition.quantity_received = quantity_received
            requisition.receipt_notes = receipt_notes
            requisition.date_received = timezone.now()
            requisition.save()
            
            # Create stock movement receipt with actual quantity received
            from .models import StockMovement
            notes = f'Received from requisition {requisition.id}'
            if receipt_notes:
                notes += f' - {receipt_notes}'
            if quantity_received < requisition.quantity_requested:
                notes += f' (Partial: {quantity_received}/{requisition.quantity_requested})'
            
            StockMovement.objects.create(
                item=requisition.item,
                movement_type='receipt',
                quantity=quantity_received,
                reference=f'Req-{requisition.id}',
                notes=notes
            )
            
            serializer = self.get_serializer(requisition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Quantity received must be a valid number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """Only admins can update requisitions."""
        if not is_admin(request.user):
            return Response(
                {'error': 'Only administrators can update requisitions.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Shared kitchen - users can delete their own requisitions, admins can delete any."""
        instance = self.get_object()
        if not is_admin(request.user):
            # Users can only delete their own requisitions
            if instance.requested_by != request.user.username:
                return Response(
                    {'error': 'You can only delete your own requisitions.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().destroy(request, *args, **kwargs)


class LowStockView(APIView):
    """
    Custom APIView to get all items with low stock levels.
    Returns items where current_stock < min_stock_level.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET endpoint at /api/low-stock/
        Returns all items where current_stock < min_stock_level (shared kitchen).
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET endpoint at /api/dashboard-stats/
        Returns JSON with aggregated stats for the shared kitchen.
        """
        try:
            # Shared kitchen - all users see all data
            total_items = Item.objects.count()
            
            # Get items with active requisitions (pending or awaiting delivery)
            active_requisition_items = Requisition.objects.filter(
                status__in=['pending', 'awaiting_delivery']
            ).values_list('item_id', flat=True)
            
            # Count low stock items EXCLUDING those with active requisitions
            low_stock_count = Item.objects.filter(
                current_stock__lt=F('min_stock_level')
            ).exclude(id__in=active_requisition_items).count()
            
            # Count pending and awaiting delivery requisitions
            pending_requisitions = Requisition.objects.filter(
                status__in=['pending', 'awaiting_delivery']
            ).count()
            
            recent_movements = StockMovement.objects.select_related('item').order_by('-date')[:5]
            recent_movements_serializer = StockMovementSerializer(recent_movements, many=True)
            
            # Calculate total stock value if prices are set
            from django.db.models import Sum, Case, When, DecimalField
            total_stock_value = Item.objects.aggregate(
                total=Sum(
                    Case(
                        When(price_per_unit__isnull=False, then=F('price_per_unit') * F('current_stock')),
                        default=0,
                        output_field=DecimalField()
                    )
                )
            )['total'] or 0
            
            stats = {
                'total_items': total_items,
                'low_stock_count': low_stock_count,
                'pending_requisitions': pending_requisitions,
                'awaiting_delivery_count': Requisition.objects.filter(status='awaiting_delivery').count(),
                'recent_movements': recent_movements_serializer.data,
                'total_stock_value': float(total_stock_value)
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
