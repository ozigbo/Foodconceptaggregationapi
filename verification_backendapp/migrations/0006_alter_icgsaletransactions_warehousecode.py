# Generated by Django 5.0.3 on 2024-03-16 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification_backendapp', '0005_alter_icgsaletransactions_warehousecode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icgsaletransactions',
            name='warehousecode',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
