# Generated by Django 3.1.7 on 2021-03-07 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20210307_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='coordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(max_length=9)),
                ('y', models.IntegerField(max_length=9)),
            ],
        ),
    ]
