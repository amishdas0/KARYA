# Generated by Django 3.1.3 on 2020-11-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20201128_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(max_length=100),
        ),
    ]
