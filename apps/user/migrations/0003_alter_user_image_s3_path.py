# Generated by Django 3.2.9 on 2022-02-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_s3_path',
            field=models.CharField(default='user-profile-photos/base_photo.png', max_length=200),
        ),
    ]
