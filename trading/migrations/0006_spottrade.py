# Generated by Django 4.0.4 on 2022-05-16 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0005_alter_spotmarket_price_increment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotTrade',
            fields=[
                ('id', models.DecimalField(db_column='ID', decimal_places=0, max_digits=11, primary_key=True, serialize=False)),
                ('price', models.DecimalField(db_column='Price', decimal_places=9, max_digits=38)),
                ('size', models.DecimalField(db_column='Size', decimal_places=9, max_digits=38)),
                ('capital', models.DecimalField(db_column='Capital', decimal_places=9, max_digits=38)),
                ('side', models.CharField(max_length=4)),
                ('liquidation', models.BooleanField(db_column='Liquidation')),
                ('time', models.DateTimeField(db_column='Time')),
                ('market', models.ForeignKey(db_column='SpotMarket', on_delete=django.db.models.deletion.CASCADE, to='trading.spotmarket')),
            ],
        ),
    ]
