# Generated by Django 4.0.4 on 2022-05-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_alter_spotmarket_price_increment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotmarket',
            name='min_provide_size',
            field=models.DecimalField(db_column='MinProvideSize', decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='spotmarket',
            name='price_increment',
            field=models.DecimalField(db_column='PriceIncrement', decimal_places=8, max_digits=9),
        ),
        migrations.AlterField(
            model_name='spotmarket',
            name='size_increment',
            field=models.DecimalField(db_column='SizeIncrement', decimal_places=6, max_digits=10),
        ),
    ]
