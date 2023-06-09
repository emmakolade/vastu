# Generated by Django 4.2 on 2023-05-01 21:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property_owner', '0001_initial'),
        ('buyers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, null=True)),
                ('edited_comment', models.BooleanField(default=False)),
                ('ratings', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('buyer_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('property_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='property_owner.propertylisting')),
            ],
        ),
    ]
