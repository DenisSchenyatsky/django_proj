# Generated by Django 5.1.6 on 2025-03-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
        migrations.AddField(
            model_name='product',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
