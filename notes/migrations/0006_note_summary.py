# Generated by Django 3.1 on 2020-08-23 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='summary',
            field=models.TextField(default='', max_length=5000),
            preserve_default=False,
        ),
    ]
