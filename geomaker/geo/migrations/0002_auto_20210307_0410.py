# Generated by Django 3.1.7 on 2021-03-07 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file_obj',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
