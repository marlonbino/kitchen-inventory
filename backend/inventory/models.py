from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Customizable categories for kitchen items.
    Only admins can manage these.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, help_text="Optional description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Item(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram (Kg)'),
        ('litre', 'Litre (L)'),
        ('piece', 'Piece'),
        ('packet', 'Packet'),
        ('dozen', 'Dozen'),
        ('bale', 'Bale'),
    ]
    
    # Shared kitchen - all items visible to all users
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price per unit in KES")
    supplier = models.CharField(max_length=200, blank=True, help_text="Supplier/Vendor name")
    min_stock_level = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_items', help_text="Who added this item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_item_name')
        ]

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        """Returns True if current_stock is below min_stock_level"""
        return self.current_stock < self.min_stock_level
    
    @property
    def total_value(self):
        """Calculate total value of current stock"""
        if self.price_per_unit and self.current_stock:
            return float(self.price_per_unit) * self.current_stock
        return 0


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('receipt', 'Receive Delivery'),
        ('usage', 'Track Usage (Cooking)'),
        ('waste', 'Track Waste/Spillage'),
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
        ('awaiting_delivery', 'Awaiting Delivery'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='requisitions'
    )
    quantity_requested = models.IntegerField()
    requested_by = models.CharField(max_length=100)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Estimated total cost for this purchase")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, help_text="Username of admin who approved the request")
    money_received_by = models.CharField(max_length=100, blank=True, help_text="Name of person who received the money for purchase")
    assigned_to = models.CharField(max_length=100, blank=True, help_text="Name of person assigned to receive delivery")
    received_by = models.CharField(max_length=100, blank=True, help_text="Name of person who confirmed receipt")
    date_received = models.DateTimeField(null=True, blank=True, help_text="Date when delivery was confirmed received")
    quantity_received = models.IntegerField(null=True, blank=True, help_text="Actual quantity received (must be <= requested)")
    receipt_notes = models.TextField(blank=True, help_text="Notes explaining any quantity discrepancies")

    class Meta:
        ordering = ['-date_requested']
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'

    def __str__(self):
        return f"{self.item.name} - {self.get_status_display()}"

    def clean(self):
        """Validate quantities"""
        if self.quantity_requested <= 0:
            raise ValidationError({'quantity_requested': 'Quantity requested must be greater than 0'})
        
        # Validate quantity_received if provided
        if self.quantity_received is not None:
            if self.quantity_received <= 0:
                raise ValidationError({'quantity_received': 'Quantity received must be greater than 0'})
            if self.quantity_received > self.quantity_requested:
                raise ValidationError({'quantity_received': 'Quantity received cannot exceed quantity requested'})
            if self.quantity_received < self.quantity_requested and not self.receipt_notes:
                raise ValidationError({'receipt_notes': 'Notes are required when quantity received is less than requested'})
    
    def save(self, *args, **kwargs):
        """Ensure validation is called on save"""
        self.full_clean()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    Extended user profile with role for kitchen management.
    """
    ROLE_CHOICES = [
        ('kitchen_staff', 'Kitchen Staff'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='kitchen_staff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class PurchaseRecord(models.Model):
    """
    Track purchases of items with prices for cost analysis.
    Only managers/admins can access this.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchase_records')
    supplier = models.CharField(max_length=200, blank=True, help_text="Where we bought from")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total paid")
    purchase_date = models.DateField()
    invoice_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Purchase Record'
        verbose_name_plural = 'Purchase Records'
        ordering = ['-purchase_date']
    
    def save(self, *args, **kwargs):
        """Calculate total amount if not provided"""
        if not self.total_amount:
            self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item.name} - {self.quantity} @ KES {self.unit_price}"


class MealCost(models.Model):
    """
    Track costs for meals (breakfast, lunch, supper).
    Only managers/admins can access this.
    """
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('supper', 'Supper'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='meal_costs')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Calculated")
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Meal Cost'
        verbose_name_plural = 'Meal Costs'
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        """Calculate total cost automatically"""
        self.total_cost = self.unit_price * self.quantity_used
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.meal_type.title()} - {self.item.name} - KES {self.total_cost}"


