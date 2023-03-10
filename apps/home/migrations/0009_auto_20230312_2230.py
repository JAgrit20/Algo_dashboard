# Generated by Django 3.2.16 on 2023-03-12 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_vwap_telegram_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_candle_conf_green',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_candle_conf_red',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_candle_exit_2_green',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_candle_exit_2_red',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_exit_70_25_rsi',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vwap_telegram_data',
            name='TV_exit_rsi_cross_down',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
