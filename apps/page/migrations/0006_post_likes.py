# Generated by Django 3.2.9 on 2022-02-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_alter_post_reply_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, to='page.Post'),
        ),
    ]
