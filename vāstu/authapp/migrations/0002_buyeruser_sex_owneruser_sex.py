# Generated by Django 4.2 on 2023-04-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyeruser',
            name='sex',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='owneruser',
            name='sex',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
