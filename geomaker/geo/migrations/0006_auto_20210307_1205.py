# Generated by Django 3.1.7 on 2021-03-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0005_auto_20210307_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinate',
            name='x',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='y_coordinate',
            name='y',
            field=models.CharField(max_length=9),
        ),
    ]