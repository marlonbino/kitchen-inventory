from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import StockMovement


@receiver(pre_save, sender=StockMovement)
def validate_stock_movement(sender, instance, **kwargs):
    """
    Validate stock movement before saving.
    Prevent negative stock for issue/writeoff movements.
    """
    # Only validate for new movements (not updates to existing ones)
    if instance.pk is None:
        item = instance.item
        movement_type = instance.movement_type
        quantity = instance.quantity

        if movement_type in ['issue', 'writeoff']:
            # Check if stock would go negative
            new_stock = item.current_stock - quantity
            if new_stock < 0:
                raise ValidationError(
                    f'Cannot {movement_type} {quantity} units. '
                    f'Current stock is only {item.current_stock} units.'
                )


@receiver(post_save, sender=StockMovement)
def update_item_stock(sender, instance, created, **kwargs):
    """
    Update Item.current_stock when a StockMovement is created.
    - On 'receipt': add quantity to current_stock
    - On 'issue' or 'writeoff': subtract quantity from current_stock
    """
    if not created:
        # Only handle new movements, not updates
        return

    item = instance.item
    movement_type = instance.movement_type
    quantity = instance.quantity

    with transaction.atomic():
        # Refresh item to get latest stock
        item.refresh_from_db()
        
        if movement_type == 'receipt':
            # Add quantity to current stock
            item.current_stock += quantity
        elif movement_type in ['issue', 'writeoff']:
            # Subtract quantity from current stock
            item.current_stock -= quantity
            # Double-check to prevent negative (should not happen due to pre_save validation)
            if item.current_stock < 0:
                item.current_stock = 0

        # Save the updated item
        item.save(update_fields=['current_stock'])

