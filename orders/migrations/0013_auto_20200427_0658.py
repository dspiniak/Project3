# Generated by Django 2.0.3 on 2020-04-27 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200427_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toppingprice',
            name='food',
            field=models.ManyToManyField(to='orders.FoodType'),
        ),
    ]
