# Generated by Django 2.0.3 on 2020-04-27 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20200427_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toppingprice',
            name='size',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Size'),
        ),
    ]
