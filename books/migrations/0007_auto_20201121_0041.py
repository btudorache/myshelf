# Generated by Django 3.1.1 on 2020-11-20 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20201021_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
