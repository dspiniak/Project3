# Generated by Django 2.0.3 on 2020-04-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200427_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseprice',
            name='size',
            field=models.ManyToManyField(to='orders.Size'),
        ),
    ]
