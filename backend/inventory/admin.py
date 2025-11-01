from django.contrib import admin
from .models import Item, StockMovement, Requisition


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'current_stock', 'min_stock_level', 'is_low_stock', 'created_at']
    list_filter = ['category', 'unit', 'created_at']  # Removed is_low_stock (property, not a field)
    search_fields = ['name', 'category']
    readonly_fields = ['created_at', 'updated_at', 'is_low_stock']
    list_editable = ['min_stock_level']
    ordering = ['name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'unit')
        }),
        ('Stock Information', {
            'fields': ('current_stock', 'min_stock_level', 'is_low_stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['item', 'movement_type', 'quantity', 'date', 'reference']
    list_filter = ['movement_type', 'date', 'item__category']
    search_fields = ['item__name', 'reference', 'notes']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    ordering = ['-date']

    fieldsets = (
        ('Movement Details', {
            'fields': ('item', 'movement_type', 'quantity', 'reference')
        }),
        ('Additional Information', {
            'fields': ('notes', 'date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity_requested', 'requested_by', 'status', 'date_requested', 'date_processed']
    list_filter = ['status', 'date_requested', 'item__category']
    search_fields = ['item__name', 'requested_by']
    readonly_fields = ['date_requested']
    date_hierarchy = 'date_requested'
    ordering = ['-date_requested']
    actions = ['approve_requisitions', 'reject_requisitions']

    fieldsets = (
        ('Requisition Details', {
            'fields': ('item', 'quantity_requested', 'requested_by', 'status')
        }),
        ('Dates', {
            'fields': ('date_requested', 'date_processed'),
            'classes': ('collapse',)
        }),
    )

    def approve_requisitions(self, request, queryset):
        """Approve selected requisitions"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='approved',
            date_processed=timezone.now()
        )
        self.message_user(request, f'{updated} requisition(s) approved.')

    approve_requisitions.short_description = 'Approve selected requisitions'

    def reject_requisitions(self, request, queryset):
        """Reject selected requisitions"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='rejected',
            date_processed=timezone.now()
        )
        self.message_user(request, f'{updated} requisition(s) rejected.')

    reject_requisitions.short_description = 'Reject selected requisitions'
