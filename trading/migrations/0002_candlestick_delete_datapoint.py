# Generated by Django 4.0.4 on 2022-06-05 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandleStick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(db_column='Market', max_length=20)),
                ('high', models.DecimalField(db_column='High', decimal_places=28, max_digits=38)),
                ('low', models.DecimalField(db_column='Low', decimal_places=28, max_digits=38)),
                ('average', models.DecimalField(db_column='Average', decimal_places=28, max_digits=38)),
                ('ema_20', models.DecimalField(db_column='EMA20', decimal_places=28, max_digits=38)),
                ('ema_50', models.DecimalField(db_column='EMA50', decimal_places=28, max_digits=38)),
                ('ema_200', models.DecimalField(db_column='EMA200', decimal_places=28, max_digits=38)),
                ('bb_plus', models.DecimalField(db_column='UpperBollingerBand', decimal_places=28, max_digits=38)),
                ('bb_minus', models.DecimalField(db_column='LowerBollingerBand', decimal_places=28, max_digits=38)),
                ('rsi', models.DecimalField(db_column='RelativeStrengthIndex', decimal_places=28, max_digits=38)),
                ('time', models.DecimalField(db_column='Time', decimal_places=6, max_digits=16)),
            ],
        ),
        migrations.DeleteModel(
            name='DataPoint',
        ),
    ]
