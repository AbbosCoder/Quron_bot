# Generated by Django 4.2.6 on 2023-10-20 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0003_alter_telegramuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='user_id',
            field=models.BigIntegerField(max_length=60, verbose_name='user_id'),
        ),
    ]
