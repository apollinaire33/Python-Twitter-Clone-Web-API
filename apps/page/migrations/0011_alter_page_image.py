# Generated by Django 3.2.9 on 2022-02-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0010_alter_page_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.CharField(default='page-profile-photos/base_photo.png', max_length=200),
        ),
    ]
