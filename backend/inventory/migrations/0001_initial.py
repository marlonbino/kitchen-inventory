# Generated manually for inventory app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Produce', 'Produce'), ('Dairy', 'Dairy'), ('Pantry', 'Pantry'), ('Meat', 'Meat'), ('Spices', 'Spices'), ('Frozen', 'Frozen'), ('Other', 'Other')], max_length=20)),
                ('unit', models.CharField(choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('lb', 'Pound'), ('oz', 'Ounce'), ('piece', 'Piece'), ('bottle', 'Bottle'), ('pack', 'Pack')], max_length=10)),
                ('min_stock_level', models.IntegerField(default=0)),
                ('current_stock', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('receipt', 'Receipt'), ('issue', 'Issue'), ('writeoff', 'Write-off')], max_length=10)),
                ('quantity', models.IntegerField()),
                ('notes', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='inventory.item')),
            ],
            options={
                'verbose_name': 'Stock Movement',
                'verbose_name_plural': 'Stock Movements',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_requested', models.IntegerField()),
                ('requested_by', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('date_processed', models.DateTimeField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisitions', to='inventory.item')),
            ],
            options={
                'verbose_name': 'Requisition',
                'verbose_name_plural': 'Requisitions',
                'ordering': ['-date_requested'],
            },
        ),
    ]

