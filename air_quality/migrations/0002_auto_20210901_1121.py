# Generated by Django 3.2.6 on 2021-09-01 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('air_quality', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='air_quality',
            name='current',
        ),
        migrations.RemoveField(
            model_name='air_quality',
            name='history',
        ),
        migrations.RemoveField(
            model_name='air_quality',
            name='prediction',
        ),
        migrations.AddField(
            model_name='air_quality',
            name='aqi',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='air_quality',
            name='pm10',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='air_quality',
            name='pm25',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='air_quality',
            name='temp',
            field=models.FloatField(default=1.0),
        ),
    ]
