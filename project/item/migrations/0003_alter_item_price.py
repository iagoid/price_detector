# Generated by Django 4.0.1 on 2022-01-25 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_item_image_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Preço'),
        ),
    ]
