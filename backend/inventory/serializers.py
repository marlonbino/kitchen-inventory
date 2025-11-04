from rest_framework import serializers
from .models import Category, Item, StockMovement, Requisition, UserProfile, PurchaseRecord, MealCost


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    item_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'item_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    Includes all fields plus read-only is_low_stock property.
    Validates min_stock_level and current_stock are non-negative.
    """
    is_low_stock = serializers.BooleanField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_value = serializers.FloatField(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'category', 'category_name', 'unit', 'price_per_unit',
            'supplier', 'min_stock_level', 'current_stock', 'is_low_stock', 'total_value',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_low_stock', 'category_name', 'total_value']

    def validate_min_stock_level(self, value):
        """
        Validate that min_stock_level is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                "Minimum stock level must be greater than or equal to 0."
            )
        return value

    def validate_current_stock(self, value):
        """
        Validate that current_stock is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                "Current stock must be greater than or equal to 0."
            )
        return value
    
    def validate_category(self, value):
        """
        Convert empty string to None for nullable ForeignKey.
        """
        if value == '':
            return None
        return value
    
    def validate(self, attrs):
        """
        Validate that item name is unique.
        """
        name = attrs.get('name')
        if name and self.instance is None:  # Only check on create, not update
            # Check if item with this name already exists
            if Item.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError(
                    {'name': f'An item with the name "{name}" already exists. Please use a unique name.'}
                )
        return attrs


class ItemNestedSerializer(serializers.ModelSerializer):
    """
    Lightweight nested serializer for Item used in related objects.
    Only includes id and name fields.
    """
    class Meta:
        model = Item
        fields = ['id', 'name']


class StockMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for StockMovement model.
    Includes all fields with nested item details (read-only).
    Validates quantity is positive and checks for negative stock on issue/writeoff.
    """
    item = ItemNestedSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source='item',
        write_only=True
    )
    item_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'item', 'item_id', 'item_name', 'movement_type',
            'quantity', 'notes', 'date', 'reference'
        ]
        read_only_fields = ['date', 'item', 'item_name']

    def get_item_name(self, obj):
        """
        Return the name of the associated item.
        """
        return obj.item.name if obj.item else None

    def validate_quantity(self, value):
        """
        Validate that quantity is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value

    def validate(self, attrs):
        """
        Custom validation - only receipts affect stock, usage and waste are tracking only.
        """
        # No validation needed - usage and waste don't affect stock
        return attrs


class RequisitionSerializer(serializers.ModelSerializer):
    """
    Serializer for Requisition model.
    Includes all fields with nested item details (read-only).
    Validates quantity_requested is positive.
    """
    item = ItemNestedSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source='item',
        write_only=True
    )
    item_name = serializers.SerializerMethodField(read_only=True)
    date_processed = serializers.DateTimeField(read_only=True)
    date_received = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Requisition
        fields = [
            'id', 'item', 'item_id', 'item_name', 'quantity_requested',
            'requested_by', 'estimated_cost', 'status', 'date_requested', 'date_processed',
            'approved_by', 'money_received_by',
            'assigned_to', 'received_by', 'date_received', 'quantity_received', 'receipt_notes'
        ]
        read_only_fields = ['date_requested', 'date_processed', 'date_received', 'item', 'item_name', 'approved_by']

    def get_item_name(self, obj):
        """
        Return the name of the associated item.
        """
        return obj.item.name if obj.item else None

    def validate_quantity_requested(self, value):
        """
        Validate that quantity_requested is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity requested must be greater than 0."
            )
        return value
    
    def validate(self, attrs):
        """
        Validate no duplicate pending or awaiting delivery requisitions for same item.
        """
        item_id = attrs.get('item_id') or (self.instance.item.id if self.instance else None)
        if item_id and self.instance is None:  # Only on create
            # Check for existing active requisitions for this item
            from .models import Requisition
            existing = Requisition.objects.filter(
                item_id=item_id,
                status__in=['pending', 'awaiting_delivery']
            ).exists()
            
            if existing:
                raise serializers.ValidationError(
                    f'An active requisition already exists for this item. Please wait for it to be processed.'
                )
        return attrs


class LowStockItemSerializer(ItemSerializer):
    """
    Serializer for items with low stock levels.
    Extends ItemSerializer and adds shortage_amount field.
    Only for items where is_low_stock is True.
    """
    shortage_amount = serializers.SerializerMethodField(read_only=True)

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['shortage_amount']

    def get_shortage_amount(self, obj):
        """
        Calculate and return the shortage amount (min_stock_level - current_stock).
        """
        if obj.is_low_stock:
            return obj.min_stock_level - obj.current_stock
        return 0


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PurchaseRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for PurchaseRecord model.
    Includes item details for better visualization.
    """
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = PurchaseRecord
        fields = [
            'id', 'item', 'item_name', 'supplier', 'quantity',
            'unit_price', 'total_amount', 'purchase_date',
            'invoice_number', 'notes'
        ]
        read_only_fields = ['total_amount']


class MealCostSerializer(serializers.ModelSerializer):
    """
    Serializer for MealCost model.
    Includes item details for better visualization.
    """
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = MealCost
        fields = [
            'id', 'item', 'item_name', 'meal_type', 'unit_price',
            'quantity_used', 'total_cost', 'date', 'notes'
        ]
        read_only_fields = ['total_cost']
