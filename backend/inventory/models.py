from django.db import models
from django.core.exceptions import ValidationError


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Produce', 'Produce'),
        ('Dairy', 'Dairy'),
        ('Pantry', 'Pantry'),
        ('Meat', 'Meat'),
        ('Spices', 'Spices'),
        ('Frozen', 'Frozen'),
        ('Other', 'Other'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('lb', 'Pound'),
        ('oz', 'Ounce'),
        ('piece', 'Piece'),
        ('bottle', 'Bottle'),
        ('pack', 'Pack'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    min_stock_level = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        """Returns True if current_stock is below min_stock_level"""
        return self.current_stock < self.min_stock_level


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('receipt', 'Receipt'),
        ('issue', 'Issue'),
        ('writeoff', 'Write-off'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='movements'
    )
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.item.name} ({self.quantity})"

    def clean(self):
        """Validate that quantity is positive"""
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than 0'})

    def save(self, *args, **kwargs):
        """Ensure validation is called on save"""
        self.full_clean()
        super().save(*args, **kwargs)


class Requisition(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='requisitions'
    )
    quantity_requested = models.IntegerField()
    requested_by = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_requested']
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'

    def __str__(self):
        return f"{self.item.name} - {self.get_status_display()}"

    def clean(self):
        """Validate that quantity_requested is positive"""
        if self.quantity_requested <= 0:
            raise ValidationError({'quantity_requested': 'Quantity requested must be greater than 0'})

    def save(self, *args, **kwargs):
        """Ensure validation is called on save"""
        self.full_clean()
        super().save(*args, **kwargs)
