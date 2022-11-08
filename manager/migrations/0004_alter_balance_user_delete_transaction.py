# Generated by Django 4.1.3 on 2022-11-04 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0003_transaction_delete_categories_delete_qq_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]