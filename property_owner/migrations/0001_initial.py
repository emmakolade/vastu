# Generated by Django 4.2 on 2023-04-29 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyOwnerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='photos/')),
                ('bio', models.TextField(blank=True)),
                ('address', models.CharField(max_length=300)),
                ('property_unit', models.IntegerField(default=0, verbose_name='number of properties')),
                ('facebook_profile', models.URLField(blank=True)),
                ('twitter_profile', models.URLField(blank=True)),
                ('instagram_profile', models.URLField(blank=True)),
                ('owner_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Owner Profiles',
            },
        ),
        migrations.CreateModel(
            name='PropertyListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=200)),
                ('property_full_address', models.CharField(max_length=200)),
                ('property_city', models.CharField(max_length=200)),
                ('property_state', models.CharField(max_length=200)),
                ('property_zipcode', models.CharField(max_length=200)),
                ('property_description', models.TextField(blank=True)),
                ('property_price', models.DecimalField(decimal_places=2, max_digits=30)),
                ('num_of_bedrooms', models.IntegerField()),
                ('num_of_bathrooms', models.IntegerField()),
                ('square_ft', models.IntegerField()),
                ('garage', models.BooleanField(default=False)),
                ('property_status', models.CharField(choices=[('FS', 'For Sale'), ('FR', 'For Rent')], max_length=8)),
                ('property_occupancy', models.CharField(choices=[('OCC', 'Occupied'), ('VAC', 'Vacant')], max_length=8)),
                ('photo_1', models.ImageField(blank=True, upload_to='photos/')),
                ('photo_2', models.ImageField(blank=True, upload_to='photos/')),
                ('photo_3', models.ImageField(blank=True, upload_to='photos/')),
                ('photo_4', models.ImageField(blank=True, upload_to='photos/')),
                ('photo_5', models.ImageField(blank=True, upload_to='photos/')),
                ('photo_6', models.ImageField(blank=True, upload_to='photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_owner.propertyownerprofile')),
            ],
        ),
    ]
