from rest_framework import serializers
from .models import Item, StockMovement, Requisition


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    Includes all fields plus read-only is_low_stock property.
    Validates min_stock_level and current_stock are non-negative.
    """
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'category', 'unit', 'min_stock_level',
            'current_stock', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_low_stock']

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
        Custom validation to check if issue/writeoff would create negative stock.
        """
        movement_type = attrs.get('movement_type')
        quantity = attrs.get('quantity')
        item = attrs.get('item')

        # Only validate for issue and writeoff types
        if movement_type in ['issue', 'writeoff'] and item:
            current_stock = item.current_stock
            new_stock = current_stock - quantity

            if new_stock < 0:
                raise serializers.ValidationError({
                    'quantity': (
                        f'Cannot {movement_type} {quantity} units. '
                        f'Current stock is only {current_stock} units. '
                        f'This would result in negative stock.'
                    )
                })

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

    class Meta:
        model = Requisition
        fields = [
            'id', 'item', 'item_id', 'item_name', 'quantity_requested',
            'requested_by', 'status', 'date_requested', 'date_processed'
        ]
        read_only_fields = ['date_requested', 'date_processed', 'item', 'item_name']

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
