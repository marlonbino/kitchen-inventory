# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_requisition_approved_by_money_received_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='estimated_cost',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Estimated total cost for this purchase', max_digits=10, null=True),
        ),
    ]
