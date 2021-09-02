# Generated by Django 3.2.6 on 2021-09-01 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Air_quality',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('current', models.JSONField()),
                ('history', models.JSONField()),
                ('prediction', models.JSONField()),
            ],
        ),
    ]
