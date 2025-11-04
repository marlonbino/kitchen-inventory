# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_update_approved_to_awaiting_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='approved_by',
            field=models.CharField(blank=True, help_text='Username of admin who approved the request', max_length=100),
        ),
        migrations.AddField(
            model_name='requisition',
            name='money_received_by',
            field=models.CharField(blank=True, help_text='Name of person who received the money for purchase', max_length=100),
        ),
    ]
