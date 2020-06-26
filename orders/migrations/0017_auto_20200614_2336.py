# Generated by Django 2.0.3 on 2020-06-14 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0016_auto_20200610_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(choices=[('1', 'pending'), ('2', 'complete')], default='1', max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='base_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='topping_price',
        ),
        migrations.AddField(
            model_name='order',
            name='order_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
