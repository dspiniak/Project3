# Generated by Django 2.0.3 on 2020-04-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200427_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtype',
            name='size',
            field=models.ManyToManyField(to='orders.Size'),
        ),
        migrations.RemoveField(
            model_name='toppingprice',
            name='food',
        ),
        migrations.AddField(
            model_name='toppingprice',
            name='food',
            field=models.ManyToManyField(blank=True, to='orders.FoodType'),
        ),
    ]