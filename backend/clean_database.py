"""
Script to clean database for production deployment.
Run this from the backend directory.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitchen_inventory.settings')
django.setup()

from inventory.models import StockMovement, Requisition
from django.db import transaction

print('\n🚀 Preparing database for production deployment...\n')

# Count before deletion
movements_count = StockMovement.objects.count()
requisitions_count = Requisition.objects.count()

print(f'📊 Test data to be removed:')
print(f'  - Stock Movements: {movements_count}')
print(f'  - Requisitions: {requisitions_count}')

# Delete test data
with transaction.atomic():
    print('\n🗑️  Removing test data...')
    
    StockMovement.objects.all().delete()
    print(f'  ✓ Deleted {movements_count} stock movements')
    
    Requisition.objects.all().delete()
    print(f'  ✓ Deleted {requisitions_count} requisitions')

print(f'\n✅ Production Database Ready!')
print(f'   All test data removed. Items, categories, and users preserved.\n')

