"""
Reset database to completely empty state - keeping ONLY users.
Deletes ALL items, categories, requisitions, and stock movements.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitchen_inventory.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Item, Category, Requisition, StockMovement

def reset_to_zero():
    print("\n" + "="*60)
    print("RESETTING DATABASE TO ZERO STATE")
    print("="*60)
    
    # Count before deletion
    requisition_count = Requisition.objects.count()
    movement_count = StockMovement.objects.count()
    item_count = Item.objects.count()
    category_count = Category.objects.count()
    user_count = User.objects.count()
    
    print(f"\nCurrent database state:")
    print(f"  - Requisitions: {requisition_count}")
    print(f"  - Stock Movements: {movement_count}")
    print(f"  - Items: {item_count}")
    print(f"  - Categories: {category_count}")
    print(f"  - Users: {user_count}")
    
    # Delete everything except users
    print("\nDeleting all data...")
    
    deleted_requisitions = Requisition.objects.all().delete()
    print(f"  [OK] Deleted {deleted_requisitions[0]} requisitions")
    
    deleted_movements = StockMovement.objects.all().delete()
    print(f"  [OK] Deleted {deleted_movements[0]} stock movements")
    
    deleted_items = Item.objects.all().delete()
    print(f"  [OK] Deleted {deleted_items[0]} items")
    
    deleted_categories = Category.objects.all().delete()
    print(f"  [OK] Deleted {deleted_categories[0]} categories")
    
    # Keep only users
    print("\nPreserved data:")
    print(f"  - Users: {User.objects.count()}")
    
    print("\n" + "="*60)
    print("DATABASE RESET TO ZERO STATE COMPLETE!")
    print("="*60)
    print("\nYour database is now completely empty except for user accounts.")
    print("You can now create fresh categories and items.")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        reset_to_zero()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

