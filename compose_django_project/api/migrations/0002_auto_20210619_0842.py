# Generated by Django 3.2.4 on 2021-06-19 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photomodel',
            name='photo',
        ),
        migrations.AddField(
            model_name='photomodel',
            name='url',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
