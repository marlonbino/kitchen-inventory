from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import StockMovement


@receiver(pre_save, sender=StockMovement)
def validate_stock_movement(sender, instance, **kwargs):
    """
    Validate stock movement before saving.
    Prevent usage on zero stock items.
    """
    if instance.movement_type == 'usage':
        # Check if item has enough stock
        item = instance.item
        if item.current_stock <= 0:
            raise ValidationError(
                f'Cannot record usage for {item.name}. Item is out of stock (current stock: {item.current_stock}).'
            )
        if item.current_stock < instance.quantity:
            raise ValidationError(
                f'Cannot record usage of {instance.quantity} for {item.name}. Only {item.current_stock} available in stock.'
            )


@receiver(post_save, sender=StockMovement)
def update_item_stock(sender, instance, created, **kwargs):
    """
    Update Item.current_stock when a StockMovement is created.
    - On 'receipt': add quantity to current_stock
    - On 'usage' or 'waste': NO change to stock (tracking only)
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
            # Receipts add to stock
            item.current_stock += quantity
            item.save(update_fields=['current_stock'])
        elif movement_type == 'usage':
            # Usage reduces stock
            item.current_stock = max(0, item.current_stock - quantity)
            item.save(update_fields=['current_stock'])
        # waste movements don't affect stock - they're just for tracking

