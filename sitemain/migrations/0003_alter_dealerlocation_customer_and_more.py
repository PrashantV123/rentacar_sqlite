# Generated by Django 4.0.3 on 2023-01-13 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sitemain', '0002_dealerlocation_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealerlocation',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_pickup_location', to='sitemain.dealerlocation'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='return_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_return_location', to='sitemain.dealerlocation'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='available_at',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitemain.dealerlocation'),
        ),
    ]
