# Generated by Django 4.2.4 on 2023-09-11 16:33

from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_paymenttype_id_alter_order_status_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_id',
            field=models.ForeignKey(default=orders.models.Status.get_default_pk, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.status'),
        ),
    ]