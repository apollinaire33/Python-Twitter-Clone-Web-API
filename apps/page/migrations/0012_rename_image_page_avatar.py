# Generated by Django 3.2.9 on 2022-02-12 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_alter_page_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='image',
            new_name='avatar',
        ),
    ]
