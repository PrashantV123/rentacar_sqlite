# Generated by Django 4.0.3 on 2023-01-16 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitemain', '0003_alter_dealerlocation_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='available',
        ),
    ]
