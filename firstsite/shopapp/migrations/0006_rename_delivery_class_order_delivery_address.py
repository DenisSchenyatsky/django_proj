# Generated by Django 5.1.6 on 2025-03-08 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivery_class',
            new_name='delivery_address',
        ),
    ]
