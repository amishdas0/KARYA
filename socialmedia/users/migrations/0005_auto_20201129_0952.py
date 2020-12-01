# Generated by Django 3.1.3 on 2020-11-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201128_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='_profile_followers_+', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='_profile_following_+', to='users.Profile'),
        ),
    ]