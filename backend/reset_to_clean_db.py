"""
Reset database to clean state - keeping only items, categories, and users.
This script removes all test data (requisitions, stock movements) for deployment.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitchen_inventory.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Item, Category, Requisition, StockMovement

def reset_database():
    print("\n" + "="*60)
    print("RESETTING DATABASE TO CLEAN STATE")
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
    
    # Delete test data
    print("\n🗑️  Deleting test data...")
    
    deleted_requisitions = Requisition.objects.all().delete()
    print(f"  ✓ Deleted {deleted_requisitions[0]} requisitions")
    
    deleted_movements = StockMovement.objects.all().delete()
    print(f"  ✓ Deleted {deleted_movements[0]} stock movements")
    
    # Keep items, categories, and users
    print("\n✅ Preserved data:")
    print(f"  - Items: {Item.objects.count()}")
    print(f"  - Categories: {Category.objects.count()}")
    print(f"  - Users: {User.objects.count()}")
    
    print("\n" + "="*60)
    print("DATABASE RESET COMPLETE!")
    print("="*60)
    print("\n✨ Your database is now clean and ready for deployment.")
    print("All items, categories, and users have been preserved.")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        reset_database()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you're in the backend directory and Django is properly configured.")

