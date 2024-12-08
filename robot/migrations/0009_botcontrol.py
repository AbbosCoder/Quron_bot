# Generated by Django 5.1.4 on 2024-12-06 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0008_menubutton'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
