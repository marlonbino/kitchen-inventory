# Generated manually for BITZ Kitchen setup with sample items

from django.db import migrations


def setup_bitz_kitchen(apps, schema_editor):
    """Set up BITZ kitchen with proper categories and sample items."""
    Category = apps.get_model('inventory', 'Category')
    Item = apps.get_model('inventory', 'Item')
    
    # Clear old categories
    Category.objects.all().delete()
    
    # Create new BITZ categories
    breakfast_category = Category.objects.create(
        name='Breakfast',
        description='Bread, milk, sugar, coffee, tea'
    )
    
    groceries_category = Category.objects.create(
        name='Groceries',
        description='Vegetables and fresh produce'
    )
    
    drinks_category = Category.objects.create(
        name='Drinks',
        description='Water and beverages'
    )
    
    meat_category = Category.objects.create(
        name='Meat',
        description='Beef and meat products'
    )
    
    cereals_category = Category.objects.create(
        name='Cereals',
        description='Kamande, Ndegu, Rice'
    )
    
    # Create sample items with Kenyan market prices (KSh)
    sample_items = [
        # Breakfast items
        {
            'name': 'Bread',
            'category': breakfast_category,
            'unit': 'piece',
            'price_per_unit': 50.00,  # KSh per loaf
            'min_stock_level': 10,
            'current_stock': 0,
            'supplier': 'Local Bakery'
        },
        {
            'name': 'Milk',
            'category': breakfast_category,
            'unit': 'litre',
            'price_per_unit': 120.00,  # KSh per litre
            'min_stock_level': 20,
            'current_stock': 0,
            'supplier': 'Fresh Dairy'
        },
        {
            'name': 'Sugar',
            'category': breakfast_category,
            'unit': 'kg',
            'price_per_unit': 180.00,  # KSh per kg
            'min_stock_level': 25,
            'current_stock': 0,
            'supplier': 'Local Market'
        },
        {
            'name': 'Coffee',
            'category': breakfast_category,
            'unit': 'kg',
            'price_per_unit': 800.00,  # KSh per kg
            'min_stock_level': 5,
            'current_stock': 0,
            'supplier': 'Coffee Supplier'
        },
        {
            'name': 'Tea',
            'category': breakfast_category,
            'unit': 'packet',
            'price_per_unit': 150.00,  # KSh per packet
            'min_stock_level': 20,
            'current_stock': 0,
            'supplier': 'Local Market'
        },
        
        # Groceries items
        {
            'name': 'Nyanya (Tomatoes)',
            'category': groceries_category,
            'unit': 'kg',
            'price_per_unit': 120.00,  # KSh per kg
            'min_stock_level': 15,
            'current_stock': 0,
            'supplier': 'Green Grocer'
        },
        {
            'name': 'Onions',
            'category': groceries_category,
            'unit': 'kg',
            'price_per_unit': 90.00,  # KSh per kg
            'min_stock_level': 20,
            'current_stock': 0,
            'supplier': 'Green Grocer'
        },
        {
            'name': 'Cabbage',
            'category': groceries_category,
            'unit': 'piece',
            'price_per_unit': 50.00,  # KSh per head
            'min_stock_level': 15,
            'current_stock': 0,
            'supplier': 'Green Grocer'
        },
        {
            'name': 'Greens',
            'category': groceries_category,
            'unit': 'bale',
            'price_per_unit': 100.00,  # KSh per bale
            'min_stock_level': 10,
            'current_stock': 0,
            'supplier': 'Local Farmer'
        },
        {
            'name': 'Eggs',
            'category': groceries_category,
            'unit': 'dozen',
            'price_per_unit': 300.00,  # KSh per dozen
            'min_stock_level': 20,
            'current_stock': 0,
            'supplier': 'Poultry Farm'
        },
        {
            'name': 'Irish Potatoes',
            'category': groceries_category,
            'unit': 'kg',
            'price_per_unit': 80.00,  # KSh per kg
            'min_stock_level': 25,
            'current_stock': 0,
            'supplier': 'Local Market'
        },
        
        # Drinks items
        {
            'name': 'Water',
            'category': drinks_category,
            'unit': 'litre',
            'price_per_unit': 40.00,  # KSh per litre
            'min_stock_level': 100,
            'current_stock': 0,
            'supplier': 'Water Supplier'
        },
        
        # Meat items
        {
            'name': 'Beef',
            'category': meat_category,
            'unit': 'kg',
            'price_per_unit': 600.00,  # KSh per kg
            'min_stock_level': 10,
            'current_stock': 0,
            'supplier': 'Butchery'
        },
        
        # Cereals items
        {
            'name': 'Kamande (Lentils)',
            'category': cereals_category,
            'unit': 'kg',
            'price_per_unit': 250.00,  # KSh per kg
            'min_stock_level': 15,
            'current_stock': 0,
            'supplier': 'Grain Market'
        },
        {
            'name': 'Ndegu (Green Grams)',
            'category': cereals_category,
            'unit': 'kg',
            'price_per_unit': 200.00,  # KSh per kg
            'min_stock_level': 15,
            'current_stock': 0,
            'supplier': 'Grain Market'
        },
        {
            'name': 'Rice',
            'category': cereals_category,
            'unit': 'kg',
            'price_per_unit': 150.00,  # KSh per kg
            'min_stock_level': 30,
            'current_stock': 0,
            'supplier': 'Grain Market'
        },
    ]
    
    for item_data in sample_items:
        Item.objects.create(**item_data)


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0006_item_supplier_alter_item_price_per_unit_and_more'),
    ]

    operations = [
        migrations.RunPython(setup_bitz_kitchen, migrations.RunPython.noop),
    ]

