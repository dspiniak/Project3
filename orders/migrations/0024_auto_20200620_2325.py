# Generated by Django 2.0.3 on 2020-06-20 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20200619_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='status',
            field=models.CharField(choices=[('unconfirmed', 'unconfirmed'), ('pending', 'pending'), ('complete', 'complete')], default='1', max_length=20),
        ),
    ]
