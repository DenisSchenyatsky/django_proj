# Generated by Django 5.1.6 on 2025-03-15 05:08

import myauth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_profile_agreement_accepted_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=myauth.models.profile_avatar_directory_path),
        ),
    ]
