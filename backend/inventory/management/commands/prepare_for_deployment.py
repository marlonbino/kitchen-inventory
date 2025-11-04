"""
Management command to prepare database for production deployment.
Removes test data while keeping essential data (items, categories, users).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Item, Category, StockMovement, Requisition
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Prepare database for production deployment by removing test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm the cleanup action',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  This command will remove all test data (requisitions and stock movements).\n'
                    'Items, categories, and users will be preserved.\n\n'
                    'Run with --confirm flag to proceed:\n'
                    'python manage.py prepare_for_deployment --confirm\n'
                )
            )
            return

        self.stdout.write(self.style.WARNING('\n🚀 Preparing database for production deployment...\n'))

        with transaction.atomic():
            # Count before deletion
            movements_count = StockMovement.objects.count()
            requisitions_count = Requisition.objects.count()
            items_count = Item.objects.count()
            categories_count = Category.objects.count()
            users_count = User.objects.count()

            self.stdout.write(f'\n📊 Current Database State:')
            self.stdout.write(f'  - Items: {items_count}')
            self.stdout.write(f'  - Categories: {categories_count}')
            self.stdout.write(f'  - Users: {users_count}')
            self.stdout.write(f'  - Stock Movements: {movements_count} (will be deleted)')
            self.stdout.write(f'  - Requisitions: {requisitions_count} (will be deleted)')

            # Delete test data
            self.stdout.write('\n🗑️  Removing test data...')
            
            StockMovement.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {movements_count} stock movements'))
            
            Requisition.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {requisitions_count} requisitions'))

            # Reset item stock levels to current_stock only (remove movement history)
            self.stdout.write('\n📦 Resetting item stock to current levels...')
            for item in Item.objects.all():
                # Keep current stock level but reset min/max if needed
                # Optionally, you could reset current_stock to 0 if you want fresh start
                pass
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ Items stock preserved'))

            # Final state
            self.stdout.write(f'\n✅ Production Database Ready!')
            self.stdout.write(f'\n📊 Final Database State:')
            self.stdout.write(f'  - Items: {Item.objects.count()} ✓')
            self.stdout.write(f'  - Categories: {Category.objects.count()} ✓')
            self.stdout.write(f'  - Users: {User.objects.count()} ✓')
            self.stdout.write(f'  - Stock Movements: {StockMovement.objects.count()} (clean)')
            self.stdout.write(f'  - Requisitions: {Requisition.objects.count()} (clean)')

            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 Database successfully prepared for production deployment!\n'
                    '   All test data removed. Items, categories, and users preserved.\n'
                )
            )

