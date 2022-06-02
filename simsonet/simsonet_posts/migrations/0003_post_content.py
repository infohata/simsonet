# Generated by Django 4.0.4 on 2022-06-01 08:17

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('simsonet_posts', '0002_alter_wall_name_alter_wall_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(default='-', verbose_name='content'),
            preserve_default=False,
        ),
    ]